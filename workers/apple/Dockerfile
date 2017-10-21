ARG DEFAULT_BASE_IMAGE
FROM ${DEFAULT_BASE_IMAGE} as compilers

ENV SDK_VERSION=10.8

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		git \
		openssl \
		patch \
		wget \
		xz-utils

WORKDIR /tmp/compile
RUN git clone https://github.com/tpoechtrager/osxcross.git . && \
	git checkout c76352d614423c54aee2b82957101a881a104c9b && \
	DEBIAN_FRONTEND=noninteractive ./tools/get_dependencies.sh && \
	wget --progress=bar:force:noscroll -P tarballs \
		https://s3.amazonaws.com/andrew-osx-sdks/MacOSX${SDK_VERSION}.sdk.tar.xz && \
	UNATTENDED=1 ./build.sh && \
	mv target /opt/osxcross && \
	mv tools /opt/osxcross && \
	ln -sf ../tools/osxcross-macports /opt/osxcross/bin/omp && \
	ln -sf ../tools/osxcross-macports /opt/osxcross/bin/osxcross-macports && \
	ln -sf ../tools/osxcross-macports /opt/osxcross/bin/osxcross-mp && \
	rm -rf /tmp/compile

WORKDIR /tmp
COPY build-ios.sh.patch build-ios.sh.patch

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
	automake \
	cmake \
	libtool

WORKDIR /tmp/compile
RUN git clone https://github.com/tpoechtrager/cctools-port.git . && \
	git checkout c1cc75893ed1978174fdcd1b898f81e6535e82d3 && \
	wget --progress=bar:force:noscroll -O iPhoneOS7.1.sdk.tar.gz \
		https://github.com/neotan/iPhoneOS7.1.sdk/archive/329870876ab9e956e24de47e92cc3ec75c1cf55a.tar.gz && \
	cd usage_examples/ios_toolchain && \
	patch -p1 < /tmp/build-ios.sh.patch && \
	./build.sh /tmp/compile/iPhoneOS7.1.sdk.tar.gz armv7 && \
	mv target /opt/ioscross/ && \
	rm -rf /tmp/compile

# Required for bundling with USE_DOCKTILEPLUGIN. lipo is a multi-architecture
# tool so it does not need to be prefixed, it just needs to be in the PATH
RUN ln -s /opt/osxcross/bin/x86_64-apple-darwin12-lipo /opt/osxcross/bin/lipo

ENV PATH=/opt/osxcross/bin:$PATH
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

FROM ${DEFAULT_BASE_IMAGE}

COPY --from=compilers /opt/osxcross /opt/osxcross
COPY --from=compilers /opt/ioscross /opt/ioscross

LABEL maintainer="ScummVM Team <admin@scummvm.org>"

ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ccache \
		clang \
		llvm-dev \
		git \
		gzip \
		make \
		python-openssl \
		python-pip \
		python-twisted \
		rsync \
		uuid-dev \
		xz-utils \
		&& \
	rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip && \
	pip --no-cache-dir install \
		buildbot-worker==${BUILDBOT_VERSION}

ENV MACOSX_DEPLOYMENT_TARGET=10.6
ENV PKG_CONFIG_PATH=/opt/osxcross/macports/pkgs/opt/local/lib/pkgconfig:$PKG_CONFIG_PATH
ENV PATH=/opt/osxcross/bin:/opt/osxcross/macports/pkgs/opt/local/bin:/opt/ioscross/bin:$PATH$PATH

# Required for bundling with USE_DOCKTILEPLUGIN
COPY arc /usr/lib/llvm-3.8/lib/arc

RUN useradd -ms /bin/bash -d /buildbot -u 2845 -U buildbot

RUN mkdir -p /data/ccache /data/sharedrepo && \
    chown buildbot:buildbot /data/ccache /data/sharedrepo

USER buildbot
WORKDIR /buildbot
COPY buildbot.tac /buildbot
CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
