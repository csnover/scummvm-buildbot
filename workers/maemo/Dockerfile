ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM debian:8
LABEL maintainer="ScummVM Team <admin@scummvm.org>"
ARG WORKER_NAME
ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}
USER root

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ccache \
		git \
		gzip \
		make \
		python-openssl \
		python-pip \
		python-twisted \
		rsync \
		xz-utils \
# Install curl for installing dumb-init
		ca-certificates \
		curl \
	&& curl -sLo /tmp/dumb-init.deb \
	https://github.com/Yelp/dumb-init/releases/download/v1.0.2/dumb-init_1.0.2_amd64.deb \
	&& dpkg -i /tmp/dumb-init.deb \
	&& rm /tmp/dumb-init.deb \
	rm -rf /var/lib/apt/lists/* && \
# Install newer version of pip to be able to install a recent buildbot
	pip install --upgrade pip && \
	/usr/local/bin/pip install --no-cache-dir \
		buildbot-worker==${BUILDBOT_VERSION}

# Install the cross-compiler
COPY ${WORKER_NAME}/diablo-toolchain.list /etc/apt/sources.list.d/
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends --force-yes \
	diablo-gcc-5 \
	diablo-package-tools \
	make \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm /etc/apt/sources.list.d/diablo-toolchain.list
RUN /opt/diablo/bin/apt-get update \
	&& /opt/diablo/bin/apt-get -y --force-yes install \
	libsdl1.2-dev \
	libpng12-dev \
	libjpeg62-dev \
	libfreetype6-dev \
	libflac-dev \
	libmad0-dev \
	libmpeg2-4-dev \
	libvorbisidec-dev \
	&& rm -rf /opt/diablo/root/var/lib/apt/lists/*

ENV PATH=$PATH:/opt/diablo/root/usr/bin:/opt/diablo/gcc-5/bin \
	OBJCOPY=arm-none-linux-gnueabi-objcopy \
	STRIP=arm-none-linux-gnueabi-strip

# Duplicate buildbot setup from default image, since we're not using that
RUN useradd -ms /bin/bash -d /buildbot -u 2845 -U buildbot

RUN mkdir -p /buildbot /data/ccache /data/sharedrepo && \
	chown buildbot:buildbot /buildbot /data/ccache /data/sharedrepo

USER buildbot
WORKDIR /buildbot

COPY common/buildbot.tac /buildbot
CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
