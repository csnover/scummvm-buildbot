from buildbot.reporters.irc import IRC

def make_services(irc_nick, irc_password, irc_channel):
    if not irc_nick or not irc_channel:
        return []

    return [
        IRC(host="irc.freenode.net",
            port=6697,
            useSSL=True,
            nick=irc_nick,
            password=irc_password,
            channels=[irc_channel],
            lostDelay=2,
            failedDelay=60,
            useRevisions=True,
            notify_events={"failureToSuccess": True, "failure": True})
    ]
