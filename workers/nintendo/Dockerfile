ARG DEFAULT_BASE_IMAGE
FROM werner/devkitpro:latest as devkitpro
FROM ${DEFAULT_BASE_IMAGE} as libraries

COPY --from=devkitpro /opt/devkitpro/devkitARM /opt/devkitpro/devkitARM
COPY --from=devkitpro /opt/devkitpro/devkitPPC /opt/devkitpro/devkitPPC
COPY --from=devkitpro /opt/devkitpro/libctru /opt/devkitpro/libctru
COPY --from=devkitpro /opt/devkitpro/libgba /opt/devkitpro/libgba
COPY --from=devkitpro /opt/devkitpro/libmirko /opt/devkitpro/libmirko
COPY --from=devkitpro /opt/devkitpro/libnds /opt/devkitpro/libnds
COPY --from=devkitpro /opt/devkitpro/libogc /opt/devkitpro/libogc

WORKDIR /tmp/compile
COPY compile-libraries.sh .
RUN ./compile-libraries.sh

FROM ${DEFAULT_BASE_IMAGE}

ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}

COPY --from=libraries /opt/devkitpro/devkitARM /opt/devkitpro/devkitARM
COPY --from=libraries /opt/devkitpro/devkitPPC /opt/devkitpro/devkitPPC
COPY --from=libraries /opt/devkitpro/libctru /opt/devkitpro/libctru
COPY --from=libraries /opt/devkitpro/libgba /opt/devkitpro/libgba
COPY --from=libraries /opt/devkitpro/libmirko /opt/devkitpro/libmirko
COPY --from=libraries /opt/devkitpro/libnds /opt/devkitpro/libnds
COPY --from=libraries /opt/devkitpro/libogc /opt/devkitpro/libogc
COPY --from=libraries /tmp/compile /tmp/compile

ENV PATH=/opt/devkitpro/devkitARM/bin:/opt/devkitpro/devkitPPC/bin:$PATH

RUN useradd -ms /bin/bash -d /buildbot -u 2845 -U buildbot
RUN mkdir -p /data/sharedrepo && chown buildbot:buildbot /data/sharedrepo

# RUN apt-get update && \
# 	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
# 		ccache \
# 		dumb-init \
# 		git \
# 		gzip \
# 		make \
# 		python-openssl \
# 		python-pip \
# 		python-twisted \
# 		rsync \
# 		xz-utils \
# 		&& \
# 	rm -rf /var/lib/apt/lists/*

# RUN pip --no-cache-dir install \
# 		buildbot-worker==${BUILDBOT_VERSION}

# USER buildbot
# WORKDIR /buildbot
# COPY buildbot.tac /buildbot
# CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
