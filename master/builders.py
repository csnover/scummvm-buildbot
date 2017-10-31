from future.utils import iteritems
from os import path

from buildbot.plugins import steps, util
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

@util.renderer
def compute_configure(props):
    repo_dir = props.getProperty("WORKER_REPO_DIR", ".")
    if repo_dir[-1] is "/":
        repo_dir = repo_dir[:-1]

    command = ["%s/configure" % repo_dir]
    args = props.getProperty("configure_args", [])
    command += args

    if ("--disable-all-engines" not in args
            and not any(arg.startswith("--enable-engine") for arg in args)):
        command.append("--enable-all-engines")

    return command

def is_not_configured(step):
    return not step.getProperty("already_configured", False)

def should_package(step):
    if step.getProperty("got_revision") and step.getProperty("package_archive_format", None) is not False:
        return True
    return False

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

def make_builder_config(repo_url, name, worker_name, config, lock, snapshots_dir, snapshots_url, snapshots_default_max):
    if snapshots_dir and snapshots_dir[-1] is not "/":
        snapshots_dir += "/"
    if snapshots_url and snapshots_url[-1] is not "/":
        snapshots_url += "/"

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
                                    doStepIf=is_not_configured))

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
        builder.addStep(steps.SetProperty(name="Computed By %s" % path.basename(__file__),
                                          property="package_name",
                                          value=compute_package_name,
                                          hideStepIf=True,
                                          doStepIf=should_package))
        builder.addStep(Package(package_name=Property("package_name"),
                                package_files=Property("package_files", None),
                                package_format=Property("package_archive_format"),
                                make_target=Property("package_make_target"),
                                strip_binaries=Property("package_strip_binaries", None),
                                env=compilation_environment,
                                doStepIf=should_package))

        source_path = Property("package_filename")
        target_path = Interpolate("%s%%(prop:package_filename)s" % snapshots_dir)
        target_url = Interpolate("%s%%(prop:package_filename)s" % snapshots_url)
        # This is not an ideal target link calculation since the archive format
        # in package_filename might be fixed up by the Package step, but here
        # only None is converted into tar.xz, which is not exactly the same
        target_link = Interpolate("%s%%(prop:buildername)s-latest."
                                  "%%(prop:package_archive_format:-tar.xz)s" % snapshots_dir)

        builder.addStep(CleaningFileUpload(name="publish",
                                           workersrc=source_path,
                                           masterdest=target_path,
                                           url=target_url,
                                           clean=True,
                                           doStepIf=should_package))
        builder.addStep(steps.MasterShellCommand(name="update latest archive",
                                                 command=["ln", "-sf", target_path, target_link],
                                                 logEnviron=False,
                                                 doStepIf=should_package))
        builder.addStep(MasterCleanSnapshots(name="clean old snapshots",
                                             workdir=snapshots_dir,
                                             file_prefix=Interpolate("%(prop:buildername)s-"),
                                             num_to_keep=Property("num_snapshots_to_keep",
                                                                  snapshots_default_max),
                                             doStepIf=should_package))

    return util.BuilderConfig(name=name,
                              workername=worker_name,
                              collapseRequests=True,
                              factory=builder,
                              nextBuild=pick_next_build,
                              locks=[lock.access("exclusive")])

def make_builders(repo_url, worker_configs, snapshots_dir=None, snapshots_url=None, snapshots_default_max=2):
    # TODO: Use one lock per container host; for now we have only one container
    # host so we just use a single lock. One lock per worker is not good enough
    # since many workers may run on a single container host and this should block
    # on host container resources.
    # "build1" is the name used for the container host in docker-compose.yml
    master_lock = util.MasterLock("build1")

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
