FROM andrewd/osxcross:4e2043771b76 as osxcross

ENV OSXCROSS_MP_INC=1
# 10.6 is the minimum version supported by macports, so either we use it for the
# deployment target or we compile all the dependencies ourselves
ENV MACOSX_DEPLOYMENT_TARGET=10.6
# libmpeg2 comes with a ton of dependencies, so is disabled for the moment
RUN echo 1 | osxcross-macports -s install \
		curl \
		faad2 \
		flac \
		freetype \
		libjpeg-turbo \
		libmad \
		libpng \
		libsdl2 \
		libsdl2_net \
		libtheora \
		libvorbis \
		zlib \
		&& \
	osxcross-macports clear-cache

LABEL maintainer="ScummVM Team <admin@scummvm.org>"

ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}

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
		&& \
	rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
ARG DUMB_INIT_URL=https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64.deb
RUN wget --progress=bar:force:noscroll $DUMB_INIT_URL && \
	dpkg --install dumb-init*.deb && \
	rm dumb-init*.deb

RUN python -m pip install --upgrade pip && \
	pip --no-cache-dir install \
		buildbot-worker==${BUILDBOT_VERSION}

# Required for bundling with USE_DOCKTILEPLUGIN. lipo is a multi-architecture
# tool so it does not need to be prefixed, it just needs to be in the PATH
COPY arc /usr/lib/llvm-3.5/lib/arc
RUN ln -s /opt/osxcross/target/bin/x86_64-apple-darwin12-lipo /opt/osxcross/target/bin/lipo

ENV PATH=/opt/osxcross/target/macports/pkgs/opt/local/bin:$PATH
ENV PKG_CONFIG_PATH=/opt/osxcross/target/macports/pkgs/opt/local/lib/pkgconfig:$PKG_CONFIG_PATH

RUN useradd -ms /bin/bash -d /buildbot -u 2845 -U buildbot

RUN mkdir -p /data/ccache /data/sharedrepo && \
    chown buildbot:buildbot /data/ccache /data/sharedrepo

USER buildbot
WORKDIR /buildbot
COPY buildbot.tac /buildbot
CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
