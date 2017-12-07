from future.utils import iteritems
from os import path
import re

from buildbot.plugins import steps, util
from .support.locks import HostLock
from .support.steps import CleaningFileUpload, FileExistsSetProperty, MasterCleanSnapshots, Package
Interpolate = util.Interpolate
Property = util.Property

GET_CPU_COUNT = "import multiprocessing; print(multiprocessing.cpu_count())"

@util.renderer
def compute_package_name(props):
    return "%s-%s" % (props.getProperty("buildername"),
                      props.getProperty("commit-description").split("/")[-1])

@util.renderer
def compute_package_filename(props):
    return "%s.%s" % (props.getProperty("package_name"),
                      props.getProperty("package_archive_format", "tar.xz"))

class BranchType:
    RELEASE, PRE_RELEASE, DEV = range(3)

def get_branch_type(branch):
    if re.match(r"v\d+", branch):
        return BranchType.RELEASE
    elif branch.startswith("branch-"):
        return BranchType.PRE_RELEASE
    else:
        return BranchType.DEV

@util.renderer
def compute_configure(props):
    repo_dir = props.getProperty("WORKER_REPO_DIR", ".")
    if repo_dir[-1] is "/":
        repo_dir = repo_dir[:-1]

    args = props.getProperty("configure_args", [])
    extra_args = props.getProperty("force_extra_configure_args", None)
    if extra_args:
        args += extra_args.split()

    command = ["%s/configure" % repo_dir] + args

    branch_type = get_branch_type(props.getProperty("branch", "master"))

    if branch_type is BranchType.RELEASE:
        command.append("--enable-release")
    elif (branch_type is BranchType.PRE_RELEASE
          and "--disable-optimizations" not in args):
        command.append("--enable-optimizations")
    elif ("--disable-all-engines" not in args
          and not any(arg.startswith("--enable-engine") for arg in args)
          and not any(arg.startswith("--disable-engine") for arg in args)):
        command.append("--enable-all-engines")

    return command

class ConfigChecker:
    last_branch_type = None
    def needs_configuration(self, step):
        # Forcing arguments invalidates any previous configuration and also
        # requires the next run to configure again with the default arguments
        if step.getProperty("force_extra_configure_args", None):
            self.last_branch_type = None
            return True

        # Changing the branch type causes conditional configure argument changes
        # in compute_configure even if all the files are the same, so must be
        # checked explicitly
        branch_type = get_branch_type(step.getProperty("branch", "master"))

        if step.getProperty("already_configured", False) is True \
            and self.last_branch_type is branch_type:
            return False

        self.last_branch_type = branch_type
        return True

def should_package(step):
    return step.getProperty("got_revision") and \
        step.getProperty("package_archive_format", None) is not False

def should_package_debug(step):
    return should_package(step) and step.getProperty("debug_package_filename")

def pick_next_build(_, build_requests):
    """
    Prefer newest build requests first.
    """
    # TODO: Cancel requested builds with source timestamp that is older
    # than the last build, so we don't backfill old builds in spare time?
    best_request = len(build_requests) and build_requests[0] or None
    for request in build_requests:
        if best_request.submittedAt < request.submittedAt:
            best_request = request
    return best_request

def make_uploader_steps(builder, snapshots_dir, snapshots_url, publish_name, property_name, latest_link, do_step_if):
    source_path = Property(property_name, None)
    target_path = Interpolate("%s%%(prop:%s)s" % (snapshots_dir, property_name))
    target_url = Interpolate("%s%%(prop:%s)s" % (snapshots_url, property_name))
    target_link = latest_link
    builder.addStep(CleaningFileUpload(name="publish %s" % publish_name,
                                       workersrc=source_path,
                                       masterdest=target_path,
                                       url=target_url,
                                       clean=True,
                                       mode=0644,
                                       doStepIf=do_step_if))
    builder.addStep(steps.MasterShellCommand(name="update latest %s" % publish_name,
                                             command=["ln", "-sf", target_path, target_link],
                                             logEnviron=False,
                                             hideStepIf=True,
                                             doStepIf=do_step_if))

def make_builder_config(repo_url, name, worker_name, config, lock, snapshots_dir, snapshots_url, snapshots_default_max):
    builder = util.BuildFactory()

    builder.addStep(steps.SetProperties(name="Worker Config File",
                                        properties=config,
                                        hideStepIf=True))

    builder.addStep(steps.SetPropertiesFromEnv(variables=["WORKER_HOST", "WORKER_REPO_DIR"],
                                               hideStepIf=True))

    # TODO: use `reference` to a common volume instead? or make the builder
    # dependent on another fetch-only builder so only one builder tries to pull it?
    builder.addStep(steps.GitHub(repourl=repo_url,
                                 workdir=Property("WORKER_REPO_DIR", None),
                                 logEnviron=False,
                                 getDescription={"always": True, "tags": True}))

    builder.addStep(FileExistsSetProperty(name="config.mk Existence Check",
                                          property="already_configured",
                                          file="%s/config.mk" % builder.workdir,
                                          hideStepIf=True))

    compilation_environment = Property("env", {})

    builder.addStep(steps.Configure(command=compute_configure,
                                    env=compilation_environment,
                                    doStepIf=ConfigChecker().needs_configuration))

    builder.addStep(steps.SetPropertyFromCommand(name="Python (Worker)",
                                                 property="cpu_count",
                                                 command=["python", "-c", GET_CPU_COUNT],
                                                 flunkOnFailure=False,
                                                 warnOnFailure=True,
                                                 hideStepIf=True,
                                                 description="getting CPU count",
                                                 descriptionDone="got CPU count"))

    # In at least Buildbot 0.9.12, warningPattern and suppressionList are not
    # renderable, so just get the properties from the config file immediately
    compiler_warning_pattern = config.get("compiler_warning_pattern",
                                          r"^([^:]+):(\d+):(?:\d+:)? [Ww]arning: (.*)$")
    compiler_warning_extractor = steps.Compile.warnExtractFromRegexpGroups
    compiler_suppression_file = Property("compiler_suppression_file", None)
    compiler_suppression_list = config.get("compiler_suppression_list", None)

    builder.addStep(steps.Compile(command=["make", Interpolate("-j%(prop:cpu_count:~1)s")],
                                  env=compilation_environment,
                                  warningPattern=compiler_warning_pattern,
                                  warningExtractor=compiler_warning_extractor,
                                  suppressionFile=compiler_suppression_file,
                                  suppressionList=compiler_suppression_list))

    builder.addStep(steps.Test(command=["make", Interpolate("%(prop:can_run_tests:"
                                                            "#?|test|test/runner)s")],
                               env=compilation_environment,
                               warningPattern=compiler_warning_pattern,
                               warningExtractor=compiler_warning_extractor,
                               suppressionFile=compiler_suppression_file,
                               suppressionList=compiler_suppression_list,
                               haltOnFailure=True,
                               flunkOnFailure=True))

    if snapshots_dir is not None and snapshots_url is not None:
        if snapshots_dir and snapshots_dir[-1] is not "/":
            snapshots_dir += "/"
        if snapshots_url and snapshots_url[-1] is not "/":
            snapshots_url += "/"

        snapshots_dir = "%s%%(prop:branch)s/" % snapshots_dir
        snapshots_url = "%s%%(prop:branch)s/" % snapshots_url

        builder.addStep(steps.SetProperty(name="Computed By %s" % path.basename(__file__),
                                          property="package_name",
                                          value=compute_package_name,
                                          hideStepIf=True,
                                          doStepIf=should_package))
        builder.addStep(Package(package_name=Property("package_name"),
                                package_files=Property("package_files", None),
                                package_format=Property("package_archive_format"),
                                make_target=Property("package_make_target"),
                                split_debug_package=Property("split_debug_package", True),
                                extra_files=Property("package_extra_files", None),
                                package_script=Interpolate(config.get("package_script", "")),
                                env=compilation_environment,
                                doStepIf=should_package))

        latest_link = Interpolate("%s%%(prop:buildername)s-latest."
                                  "%%(prop:package_archive_format:-tar.xz)s" % snapshots_dir)
        make_uploader_steps(builder=builder,
                            snapshots_dir=snapshots_dir,
                            snapshots_url=snapshots_url,
                            publish_name="archive",
                            property_name="package_filename",
                            latest_link=latest_link,
                            do_step_if=should_package)

        latest_link = Interpolate("%s%%(prop:buildername)s"
                                  "-latest-debug-symbols.tar.xz" % snapshots_dir)
        make_uploader_steps(builder=builder,
                            snapshots_dir=snapshots_dir,
                            snapshots_url=snapshots_url,
                            publish_name="debug archive",
                            property_name="debug_package_filename",
                            latest_link=latest_link,
                            do_step_if=should_package_debug)

        builder.addStep(MasterCleanSnapshots(name="clean old snapshots",
                                             workdir=Interpolate(snapshots_dir),
                                             file_prefix=Interpolate("%(prop:buildername)s-"),
                                             num_to_keep=Property("num_snapshots_to_keep",
                                                                  snapshots_default_max),
                                             secondary_file_suffix="-debug-symbols",
                                             file_extensions=r"\.(?:tar(?:\.[xg]z)?|[a-z]{3,4})$",
                                             doStepIf=should_package,
                                             hideStepIf=True))

    return util.BuilderConfig(name=name,
                              workername=worker_name,
                              collapseRequests=True,
                              factory=builder,
                              nextBuild=pick_next_build,
                              locks=[lock.access("counting")])

def make_builders(repo_url, worker_configs, snapshots_dir=None, snapshots_url=None, snapshots_default_max=2):
    master_lock = HostLock("builds")

    builders = []
    for (worker_name, worker_config) in iteritems(worker_configs):
        for (builder_name, builder_config) in iteritems(worker_config["builders"]):
            # Workers with only one builder give it a blank name
            if not builder_name:
                builder_name = worker_name
            else:
                builder_name = "%s-%s" % (worker_name, builder_name)

            builders.append(make_builder_config(repo_url=repo_url,
                                                name=builder_name,
                                                worker_name=worker_name,
                                                config=builder_config,
                                                lock=master_lock,
                                                snapshots_dir=snapshots_dir,
                                                snapshots_url=snapshots_url,
                                                snapshots_default_max=snapshots_default_max))

    return builders
