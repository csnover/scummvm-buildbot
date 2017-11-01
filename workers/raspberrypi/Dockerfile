ARG DEFAULT_BASE_IMAGE
FROM sdthirlwall/raspberry-pi-cross-compiler@sha256:f14f0bd23e766ed40ec109d9fe98aab68229b5ccce1d4acde09327549e1588d7
LABEL maintainer="ScummVM Team <admin@scummvm.org>"
USER root
ARG WORKER_NAME

ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}

# Install dumb-init manually, since this image is based on Debian jessie.
RUN curl -L -o dumb-init_1.2.0_amd64.deb https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64.deb && \
	dpkg -i dumb-init_*.deb && \
	rm dumb-init_*.deb && \
# Install system packages for buildbot
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ccache \
		git \
		gzip \
		make \
		python-openssl \
		python-pip \
		python-twisted \
		rsync \
		xz-utils && \
	rm -rf /var/lib/apt/lists/* && \
# Install newer version of pip to be able to install a recent buildbot
	pip install --upgrade pip && \
	/usr/local/bin/pip install --no-cache-dir \
		buildbot-worker==${BUILDBOT_VERSION}

# Install raspbian packages for the cross-compilation environment
RUN rpdo apt-get update && install-raspbian -y --no-install-recommends \
		libsdl2-dev \
		libpng12-dev \
		zlib1g-dev \
		libfaad-dev \
		libflac-dev \
		libmad0-dev \
		libjpeg62-turbo-dev \
		libfreetype6-dev \
		libfluidsynth-dev \
		libvorbisidec-dev \
		libvorbis-dev \
		libtheora-dev \
		libmpeg2-4-dev \
		libcurl4-openssl-dev \
		libsdl2-net-dev && \
	rpdo rm -rf /var/lib/apt/lists/*

# Duplicate buildbot setup from default image, since we're not using that
RUN useradd -ms /bin/bash -d /buildbot -u 2845 -U buildbot

RUN mkdir -p /buildbot /data/ccache /data/sharedrepo && \
	chown buildbot:buildbot /buildbot /data/ccache /data/sharedrepo

USER buildbot
WORKDIR /buildbot

COPY common/buildbot.tac /buildbot
CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
