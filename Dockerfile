FROM buildbot/buildbot-master:v0.9.12
COPY master.cfg /var/lib/buildbot
COPY secrets.cfg /var/lib/buildbot
COPY master /var/lib/buildbot/master
COPY workers /var/lib/buildbot/workers
RUN apk add --no-cache py-requests py-certifi
