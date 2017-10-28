ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE}
LABEL maintainer="ScummVM Team <admin@scummvm.org>"
ARG WORKER_NAME

ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ccache \
		dumb-init \
		git \
		gzip \
		make \
		python-openssl \
		python-pip \
		python-twisted \
		rsync \
		xz-utils \
		&& \
	rm -rf /var/lib/apt/lists/*

RUN pip --no-cache-dir install \
		buildbot-worker==${BUILDBOT_VERSION}

RUN useradd -ms /bin/bash -d /buildbot -u 2845 -U buildbot

RUN mkdir -p /buildbot /data/ccache /data/sharedrepo && \
	chown buildbot:buildbot /buildbot /data/ccache /data/sharedrepo

COPY ${WORKER_NAME}/buildbot.tac /buildbot

USER buildbot
WORKDIR /buildbot
CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
