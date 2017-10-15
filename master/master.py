from os import environ, listdir, path
from logging import warning
from runpy import run_path
import re

from buildbot.data import resultspec
from buildbot.process.results import SUCCESS
from twisted.internet import defer, reactor

from .builders import make_builders
from .caches import make_caches
from .configurators import make_configurators
from .database import make_database
from .protocols import make_protocols
from .schedulers import make_schedulers
from .services import make_services
from .workers import make_workers
from .www import make_www

def maybe_int(value):
    try:
        return int(value)
    except ValueError:
        return value

def make_builder_names(worker_configs):
    builder_names = []
    for (worker_name, worker_config) in worker_configs.iteritems():
        for builder_name in worker_config["builders"].keys():
            if not builder_name:
                builder_name = worker_name
            else:
                builder_name = "%s-%s" % (worker_name, builder_name)

            builder_names.append(builder_name)

    return builder_names

class DebouncedBuilderPrioritizer:
    """
    BuildBot sends single builders to prioritizeBuilders, even when multiple
    builders are eligible for a given changeset. To deal with this, we use a
    simple time-based debouncer that collects all the builders and only
    returns an actual list of builders to use to the build master once things
    have settled down.
    """
    timer = None
    master = None
    builders = {}
    deferred = None

    def __init__(self, timeout):
        self.timeout = timeout

    def debounce_prioritize(self, master, builders):
        # Don't debounce any of the system-generated builders
        if len(builders) == 1 and builders[0].name.startswith("__"):
            return defer.succeed(builders)

        if self.timer:
            self.timer.reset()
        else:
            self.timer = reactor.callLater(self.timeout, self.commit)
        if self.deferred:
            self.deferred.callback([])
        self.deferred = defer.Deferred()
        self.master = master
        for builder in builders:
            self.builders[builder.name] = builder
        return self.deferred

    def commit(self):
        self.timer = None
        deferred = self.deferred
        self.deferred = None
        self.prioritize().chainDeferred(deferred)

    @defer.inlineCallbacks
    def prioritize(self):
        """
        Prefer failed builders first.
        """
        assert self.master
        builder_priorities = []
        for builder in self.builders.itervalues():
            builder_id = yield builder.getBuilderId()
            builds = yield self.master.data.get(("builds",),
                                                filters=[resultspec.Filter("builderid", "eq", [builder_id]),
                                                         resultspec.Filter("results", "ne", [None])],
                                                order=["-number"],
                                                limit=1)

            if builds and builds[0]['results'] == SUCCESS:
                priority = 1
            else:
                priority = 0

            builder_priorities.append((builder, priority))

        self.master = None
        self.builders.clear()

        builder_priorities.sort(key=lambda bp: bp[1])
        defer.returnValue([bp[0] for bp in builder_priorities])

def make_buildmaster_config():
    secrets = run_path(path.join(path.dirname(__file__), "..", "secrets.cfg"))

    worker_configs = {}
    workers_dir = path.realpath(path.join(path.dirname(__file__), "..", "workers"))

    for worker_name in listdir(workers_dir):
        if worker_name == "_template":
            continue

        worker_config_filename = path.join(workers_dir, worker_name, "buildbot.cfg")
        if path.exists(worker_config_filename):
            try:
                worker_config = run_path(worker_config_filename)
                if "builders" not in worker_config:
                    raise KeyError("Required key 'builders' is missing from worker configuration")
                worker_configs[worker_name] = worker_config
            except Exception, e:
                warning("Could not load configuration for worker %s: %s", worker_name, e)

    repo_url = environ.get("BUILDBOT_REPO_URL")
    assert repo_url
    repo_info = re.match(r"^(.*?(([^/]+)\/([^/]+)))\.git$", repo_url)
    assert repo_info
    (repo_id, project_id, org_id) = repo_info.group(1, 2, 3)

    worker_port = maybe_int(environ.get("BUILDBOT_WORKER_PORT", 28459))
    is_dev_env = environ.get("BUILDBOT_DEV_ENV", False)
    irc_username = environ.get("BUILDBOT_IRC_USERNAME")
    irc_channel = environ.get("BUILDBOT_IRC_CHANNEL")
    snapshots_default_max = environ.get("SCUMMVM_SNAPSHOTS_DEFAULT_MAX", 2)
    admin_role = environ.get("BUILDBOT_ADMIN_ROLE", org_id)

    required_secrets = ["github_hook_secret", "worker_password"]
    if is_dev_env is not True:
        required_secrets += ["github_client_id", "github_client_secret"]
    if irc_username and irc_channel:
        required_secrets.append("irc_password")
    for key in required_secrets:
        if key not in secrets:
            raise KeyError("Required key '%s' is missing from secrets configuration" % key)

    prioritizer = DebouncedBuilderPrioritizer(1.0)

    config = {
        "buildbotURL": environ.get("BUILDBOT_WEB_URL"),
        "buildbotNetUsageData": "basic",
        "builders": make_builders(repo_url=repo_url,
                                  worker_configs=worker_configs,
                                  snapshots_dir=environ.get("SCUMMVM_SNAPSHOTS_DIR"),
                                  snapshots_url=environ.get("SCUMMVM_SNAPSHOTS_URL"),
                                  snapshots_default_max=snapshots_default_max),
        "caches": make_caches(),
        "configurators": make_configurators(),
        "db": make_database(environ.get("BUILDBOT_DATABASE")),
        "prioritizeBuilders": prioritizer.debounce_prioritize,
        "protocols": make_protocols(worker_port),
        "schedulers": make_schedulers(make_builder_names(worker_configs), project_id, repo_id),
        "services": make_services(irc_username, secrets["irc_password"], irc_channel),
        "title": environ.get("BUILDBOT_SITE_TITLE"),
        "titleURL": environ.get("BUILDBOT_SITE_URL"),
        "workers": make_workers(worker_configs.keys(), secrets),
        "www": make_www(environ.get("BUILDBOT_WEB_PORT"), admin_role, secrets, is_dev_env)
    }

    return config
