from os import listdir, lstat, path, unlink
import re

from buildbot.plugins import steps
from buildbot.status import builder
from buildbot.process.buildstep import BuildStep, BuildStepFailed, ShellMixin
from buildbot.process.remotecommand import RemoteShellCommand
from buildbot.steps.worker import CompositeStepMixin
from twisted.internet import defer

class CleaningFileUpload(steps.FileUpload):
    name = "CleaningFileUpload"
    descriptionDone = "uploaded"

    def __init__(self, clean=False, **kwargs):
        super(CleaningFileUpload, self).__init__(**kwargs)
        self.clean = clean

    @defer.inlineCallbacks
    def finished(self, results):
        if self.clean:
            cmd = RemoteShellCommand(command=["rm", self.workersrc],
                                     workdir=self.workdir,
                                     logEnviron=False)
            yield self.runCommand(cmd)
            if cmd.didFail():
                results = builder.WARNINGS
        return_value = yield super(CleaningFileUpload, self).finished(results)
        defer.returnValue(return_value)

class FileExistsSetProperty(steps.FileExists):
    name = "FileExistsSetProperty"
    renderables = ["property", "file"]

    def __init__(self, property, file, **kwargs):
        self.property = property
        super(FileExistsSetProperty, self).__init__(file, **kwargs)

    def commandComplete(self, cmd):
        self.setProperty(self.property, not cmd.didFail(), self.name)
        self.finished(builder.SUCCESS)

class MasterCleanSnapshots(BuildStep):
    name = "MasterCleanSnapshots"
    description = "cleaning"
    descriptionDone = "cleaned"
    flunkOnFailure = False
    haltOnFailure = False
    warnOnFailure = True

    renderables = ["file_prefix", "num_to_keep", "secondary_file_suffix"]

    def __init__(self, file_prefix, num_to_keep, secondary_file_suffix=None, **kwargs):
        super(MasterCleanSnapshots, self).__init__(**kwargs)
        self.file_prefix = file_prefix
        self.num_to_keep = num_to_keep
        self.secondary_file_suffix = secondary_file_suffix

    def add_to_matches(self, matches, created_at, file_path):
        # TODO: This is all a pretty dumb way of doing this

        base_name = re.sub(r"\.(?:tar(?:\.[xg]z)?|zip)$", "", file_path)
        if base_name.endswith(self.secondary_file_suffix):
            prefix = base_name.rpartition(self.secondary_file_suffix)[0]
            try:
                match = next(match for match in matches \
                    if match[1] and match[1].startswith(prefix))
                match[2] = file_path
            except StopIteration:
                matches.append([0, None, file_path])
        else:
            try:
                match = next(match for match in matches \
                    if match[2] and match[2].startswith(base_name))
                match[0] = created_at
                match[1] = file_path
            except StopIteration:
                matches.append([created_at, file_path, None])

    @defer.inlineCallbacks
    def run(self):
        self.updateSummary()
        log = yield self.addLog("log", "t")

        matches = []
        log.addContent(u"Looking for candidates matching %s*\n" % self.file_prefix)
        for file_name in listdir(self.workdir):
            file_path = path.join(self.workdir, file_name)
            if path.islink(file_path):
                continue
            if path.isfile(file_path) and file_name.startswith(self.file_prefix):
                log.addContent(u"Matched %s\n" % file_name)
                created_at = path.getctime(file_path)
                self.add_to_matches(matches, created_at, file_path)

        matches.sort(key=lambda match: match[0])
        if len(matches) > self.num_to_keep:
            for [_, file_path, secondary_file_path] in matches[:-self.num_to_keep]:
                log.addContent(u"Unlinking %s\n" % path.basename(file_path))
                unlink(file_path)
                if secondary_file_path:
                    log.addContent(u"Unlinking %s\n" % path.basename(file_path))
                    unlink(secondary_file_path)
        else:
            log.addContent("Already clean\n")

        self.descriptionDone = "cleaned %d files" % max(0, len(matches) - self.num_to_keep)
        defer.returnValue(builder.SUCCESS)

class Package(BuildStep, ShellMixin, CompositeStepMixin):
    SPLIT_DEBUG_SYMBOLS_SCRIPT = """
        set -e
        strip=%s
        objcopy=%s
        for file in %s; do
            echo $file
            $strip --only-keep-debug -o "$file.dbg" "$file"
            $strip -o "$file.st" "$file"
            mv "$file" "$file.orig"
            mv "$file.st" "$file"
            $objcopy --add-gnu-debuglink="$file.dbg" "$file" || true
        done
    """

    RESTORE_UNSTRIPPED_BINARIES_SCRIPT = """
        set -e
        for debug_file in %s; do
            orig_file=${debug_file%%.dbg}
            echo $orig_file
            mv "$orig_file.orig" "$orig_file"
            rm "$debug_file"
        done
    """

    name = "package"
    flunkOnFailure = True
    haltOnFailure = True
    description = "packaging"
    descriptionDone = "packaged"

    renderables = ["make_target",
                   "package_name",
                   "package_files",
                   "package_format",
                   "split_debug_package"]

    def __init__(self, package_name, package_format="tar.xz",
                 package_files=None, make_target=None,
                 split_debug_package=False,
                 **kwargs):
        kwargs = self.setupShellMixin(kwargs, prohibitArgs=["command"])
        super(Package, self).__init__(**kwargs)
        assert package_name
        self.package_name = package_name
        self.package_format = package_format
        self.package_files = package_files
        self.make_target = make_target
        self.split_debug_package = split_debug_package
        self.packaging_results = builder.SUCCESS

    @defer.inlineCallbacks
    def send_command(self, **kwargs):
        cmd = yield self.makeRemoteShellCommand(**kwargs)
        yield self.runCommand(cmd)
        if cmd.didFail():
            raise BuildStepFailed(cmd.stderr.strip())
        self.updateSummary()
        if kwargs.get("collectStderr", False):
            defer.returnValue(cmd.stderr.strip())
        else:
            defer.returnValue(cmd.stdout.strip())

    @defer.inlineCallbacks
    def make_default_bundle(self, executable_files):
        bundle_dir = self.package_name
        dist_files = yield self.send_command(command=["make", "print-dists"],
                                             collectStdout=True,
                                             logEnviron=False)
        yield self.runRmdir(path.join(self.workdir, bundle_dir))
        yield self.runMkdir(path.join(self.workdir, bundle_dir))
        yield self.send_command(command=["rsync", "-aRv",
                                         executable_files, bundle_dir],
                                logEnviron=False)
        if dist_files:
            yield self.send_command(command=["cp", "-a", dist_files.split(" "), bundle_dir],
                                    logEnviron=False)
        defer.returnValue([bundle_dir + "/"])

    @defer.inlineCallbacks
    def get_from_env(self, key, default):
        if self.env and self.env.has_key(key):
            defer.returnValue(self.env[key])
            return

        builder_env = yield self.build.render(self.build.builder.config.env)
        if builder_env and builder_env.has_key(key):
            defer.returnValue(builder_env[key])
            return

        worker_env = self.worker.worker_environ
        if worker_env and worker_env.has_key(key):
            defer.returnValue(worker_env[key])
            return

        defer.returnValue(default)

    @defer.inlineCallbacks
    def split_debug_files(self, executable_files):
        strip = yield self.get_from_env("STRIP", "strip")
        objcopy = yield self.get_from_env("OBJCOPY", "objcopy")

        split_script = self.SPLIT_DEBUG_SYMBOLS_SCRIPT % (strip,
                                                          objcopy,
                                                          " ".join(executable_files))
        warnings = yield self.send_command(command=["/usr/bin/env", "bash", "-c", split_script],
                                           logEnviron=False,
                                           collectStderr=True)

        # Setting up the debug link is not critical and fails for a.out
        # executable types
        if warnings:
            self.addCompleteLog("warnings (%d)" % (warnings.count("\n") + 1), warnings + "\n")
            self.packaging_results = builder.WARNINGS

        debug_files = [[], []]
        for file_name in executable_files:
            debug_file_name = file_name + ".dbg"
            debug_files[0].append(debug_file_name)
            has_dwp = yield self.pathExists(path.join(self.workdir, file_name + ".dwp"))
            if has_dwp:
                debug_files[1].append(file_name + ".dwp")

        defer.returnValue(debug_files)

    @defer.inlineCallbacks
    def run(self):
        self.packaging_results = builder.SUCCESS
        if self.split_debug_package or self.make_target is None:
            executable_files = yield self.send_command(command=["make", "print-executables"],
                                                       collectStdout=True,
                                                       logEnviron=False)
            assert executable_files
            executable_files = executable_files.split(" ")

        if self.split_debug_package:
            debug_files = yield self.split_debug_files(executable_files)
        else:
            debug_files = None

        # TODO: Make Makefile always bundle with `make bundle`, and get rid of
        # this extra machinery just for CI
        if self.make_target is None:
            package_files = yield self.make_default_bundle(executable_files)
        else:
            if self.package_files:
                package_files = self.package_files
            else:
                package_files = [self.make_target + "/"]
                yield self.runRmdir(path.join(self.workdir, self.make_target))

            yield self.send_command(command=["make", self.make_target])

        package_format = self.package_format
        if package_format is "zip":
            archiver = ["zip", "-8r"]
            compression_options = {}
        else:
            if package_format is "tar.gz":
                compression_flag = "j"
                compression_options = {"GZIP": "-9"}
            elif package_format is "tar":
                compression_flag = ""
                compression_options = {}
            else:
                compression_flag = "J"
                compression_options = {"XZ_OPT": "-2"}
                package_format = "tar.xz"

            archiver = ["tar", "-cv%sf" % compression_flag]

        archive_filename = "%s.%s" % (self.package_name, package_format)
        archiver.append(archive_filename)
        archiver += package_files

        yield self.send_command(command=archiver, env=compression_options, logEnviron=False)
        yield self.send_command(command=["rm", "-r", package_files], logEnviron=False)
        self.setProperty("package_filename", archive_filename)

        if debug_files:
            debug_archive_filename = "%s-debug-symbols.tar.xz" % self.package_name
            yield self.send_command(command=["tar", "-cvJf",
                                             debug_archive_filename,
                                             debug_files],
                                    env={"XZ_OPT": "-2"},
                                    logEnviron=False)
            # The unstripped executables need to be restored after packaging to
            # prevent crashes if the next build does not relink executables
            restore_script = self.RESTORE_UNSTRIPPED_BINARIES_SCRIPT % " ".join(debug_files[0])
            yield self.send_command(command=["/usr/bin/env", "bash", "-c", restore_script],
                                    logEnviron=False)
            self.setProperty("debug_package_filename", debug_archive_filename)

        defer.returnValue(self.packaging_results)
