FROM i386/debian:9.2
LABEL maintainer="ScummVM Team <admin@scummvm.org>"

ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}

ARG URL=http://www.gcw-zero.com/files/opendingux-gcw0-toolchain.2014-08-20.tar.bz2
ARG SHASUM=c5ec0402fdbea95a537b1d8ad9cf905572cb7265319483dc54c3b1e1daee2a08cadb84aa81d88c41dcfaa04423706e48

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		bzip2 \
		ca-certificates \
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
		wget && \
	rm -rf /var/lib/apt/lists/* && \
	wget --progress=bar:force:noscroll -O gcw0.tar.bz2 ${URL} && \
	echo "$SHASUM *gcw0.tar.bz2" | sha384sum -c && \
	tar xjf gcw0.tar.bz2 && \
	rm gcw0.tar.bz2 && \
	pip --no-cache-dir install \
		buildbot-worker==${BUILDBOT_VERSION}

ENV PATH=/opt/gcw0-toolchain/usr/bin:$PATH

RUN useradd -ms /bin/bash -d /buildbot -u 2845 -U buildbot

RUN mkdir -p /buildbot /data/ccache /data/sharedrepo && \
	chown buildbot:buildbot /buildbot /data/ccache /data/sharedrepo

COPY common/buildbot.tac /buildbot

USER buildbot
WORKDIR /buildbot
CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
