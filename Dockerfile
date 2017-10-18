# Changes to the Buildbot version here will be picked up by build-images.sh
FROM buildbot/buildbot-master:v0.9.12

RUN apk add --no-cache \
    py-certifi \
    py-requests \
    shadow
RUN useradd -ms /bin/bash -d /var/lib/buildbot -u 2845 -U buildbot && \
    chown -R buildbot:buildbot /var/lib/buildbot
RUN mkdir -p /data/db /data/snapshots && \
    chown buildbot:buildbot /data/db /data/snapshots
USER buildbot
WORKDIR /var/lib/buildbot
COPY master.cfg .
COPY master master
