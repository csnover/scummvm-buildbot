from os import environ, listdir, path
from logging import warning
from runpy import run_path
import re

from buildbot.data import resultspec
from buildbot.process.results import SUCCESS
from twisted.internet import defer

from .builders import make_builders
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

@defer.inlineCallbacks
def pick_builder(master, builders):
    """
    Prefer failed builders first.
    """
    builder_priorities = []
    for builder in builders:
        builder_id = yield builder.getBuilderId()
        builds = yield master.data.get(("builds",),
                                       filters=[resultspec.Filter("builderid", "eq", [builder_id]),
                                                resultspec.Filter("complete", "eq", [True])],
                                       order=["-number"],
                                       limit=1)

        if builds and builds[0]['results'] == SUCCESS:
            priority = 1
        else:
            priority = 0

        builder_priorities.append((builder, priority))

    def key_sort(builder):
        for (candidate_builder, priority) in builder_priorities:
            if builder is candidate_builder:
                return priority
        assert 0

    builders.sort(key=key_sort)
    defer.returnValue(builders)

def make_buildmaster_config():
    secrets = run_path(path.join(path.dirname(__file__), "_secrets.py"))

    worker_configs = {}
    workers_dir = path.realpath(path.join(path.dirname(__file__), "../workers"))

    for worker_name in listdir(workers_dir):
        worker_config_filename = path.join(workers_dir, worker_name, "buildbot.cfg")
        if path.exists(worker_config_filename):
            try:
                worker_config = run_path(worker_config_filename)
                if "builders" not in worker_config:
                    raise KeyError("Required key 'builders' is missing from worker configuration")
                worker_configs[worker_name] = worker_config
            except Exception, e:
                warning("Could not load configuration for worker %s: %s", worker_name, e)

    worker_port = maybe_int(environ.get("BUILDBOT_WORKER_PORT", 28459))
    is_dev_env = environ.get("BUILDBOT_DEV_ENV", False)
    irc_username = environ.get("BUILDBOT_IRC_USERNAME")
    irc_channel = environ.get("BUILDBOT_IRC_CHANNEL")

    repo_url = environ.get("BUILDBOT_REPO_URL")
    assert repo_url
    repo_info = re.match(r"^(.*?(([^/]+)\/([^/]+)))\.git$", repo_url)
    assert repo_info
    (repo_id, project_id, org_id) = repo_info.group(1, 2, 3)

    config = {
        "buildbotURL": environ.get("BUILDBOT_WEB_URL"),
        "buildbotNetUsageData": "basic",
        "builders": make_builders(repo_url=repo_url,
                                  worker_configs=worker_configs,
                                  snapshots_dir=environ.get("SCUMMVM_SNAPSHOTS_DIR"),
                                  snapshots_url=environ.get("SCUMMVM_SNAPSHOTS_URL")),
        "configurators": make_configurators(),
        "db": make_database(environ.get("BUILDBOT_DATABASE")),
        "prioritizeBuilders": pick_builder,
        "protocols": make_protocols(worker_port),
        "schedulers": make_schedulers(make_builder_names(worker_configs), project_id, repo_id),
        "services": make_services(irc_username, secrets["irc_password"], irc_channel),
        "title": environ.get("BUILDBOT_SITE_TITLE"),
        "titleURL": environ.get("BUILDBOT_SITE_URL"),
        "workers": make_workers(worker_configs.keys(), secrets),
        "www": make_www(environ.get("BUILDBOT_WEB_PORT"), environ.get("BUILDBOT_ADMIN_ROLE", org_id), secrets, is_dev_env)
    }

    return config
