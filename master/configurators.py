from datetime import timedelta
from buildbot.plugins import util
JanitorConfigurator = util.JanitorConfigurator

def make_configurators():
    return [
        JanitorConfigurator(logHorizon=timedelta(weeks=2),
                            hour=12,
                            dayOfWeek=1)
    ]
