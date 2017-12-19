ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE} as compilers
USER root
ARG WORKER_NAME

ARG SDK_VERSION=10.8

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		git \
		openssl \
		patch \
		wget \
		xz-utils

# macOS cross-compiler
# The andrew-osx-sdks URL comes from the andrewd/osxcross image
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

# Required for bundling with USE_DOCKTILEPLUGIN. lipo is a multi-architecture
# tool so it does not need to be prefixed, it just needs to be in the PATH
RUN ln -s /opt/osxcross/bin/x86_64-apple-darwin12-lipo /opt/osxcross/bin/lipo

ENV PATH=/opt/osxcross/bin:$PATH
# 10.6 is the minimum version supported by macports, so either we use it for the
# deployment target or we compile all the dependencies ourselves
ENV MACOSX_DEPLOYMENT_TARGET=10.6

# libmpeg2 comes with a ton of dependencies because the osxcross macports script
# does not understand variants, so is disabled for the moment
RUN echo 1 | VERBOSE=1 osxcross-macports -s install \
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

# dpkg-dev is required to retrieve sources from apt
RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dpkg-dev \
		pkg-config

ENV PATH=$PATH:/opt/osxcross/bin:/opt/osxcross/macports/pkgs/opt/local/bin

WORKDIR /tmp/compile
COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-macos.sh ./

COPY common/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-macos.sh mpeg2dec

COPY ${WORKER_NAME}/library-rules/fluidsynth-lite.sh library-rules/
COPY ${WORKER_NAME}/fluidsynth-lite-macos.patch ./
RUN ./compile-libraries-macos.sh fluidsynth-lite

FROM ${DEFAULT_BASE_IMAGE}
USER root
ARG WORKER_NAME

COPY --from=compilers /opt/osxcross /opt/osxcross

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		clang \
		llvm-dev \
		uuid-dev \
		&& \
	rm -rf /var/lib/apt/lists/*

ENV MACOSX_DEPLOYMENT_TARGET=10.6
ENV OSXCROSS_MP_INC=1

# Required for bundling with USE_DOCKTILEPLUGIN
COPY ${WORKER_NAME}/arc /usr/lib/llvm-3.8/lib/arc

ARG SDK_VERSION=10.8

ENV PATH=$PATH:/opt/osxcross/bin:/opt/osxcross/macports/pkgs/opt/local/bin:/opt/osxcross/SDK/MacOSX${SDK_VERSION}.sdk/usr/bin \
	OBJECTDUMP=x86_64-apple-darwin12-ObjectDump \
	AR=x86_64-apple-darwin12-ar \
	AS=x86_64-apple-darwin12-as \
	BITCODE_STRIP=x86_64-apple-darwin12-bitcode_strip \
	CXX=x86_64-apple-darwin12-c++ \
	CC=x86_64-apple-darwin12-cc \
	CHECK_DYLIB=x86_64-apple-darwin12-check_dylib \
	CHECKSYMS=x86_64-apple-darwin12-checksyms \
	CMPDYLIB=x86_64-apple-darwin12-cmpdylib \
	CODESIGN_ALLOCATE=x86_64-apple-darwin12-codesign_allocate \
	DSYMUTIL=x86_64-apple-darwin12-dsymutil \
	INDR=x86_64-apple-darwin12-indr \
	INOUT=x86_64-apple-darwin12-inout \
	INSTALL_NAME_TOOL=x86_64-apple-darwin12-install_name_tool \
	LD=x86_64-apple-darwin12-ld \
	LIBTOOL=x86_64-apple-darwin12-libtool \
	LIPO=x86_64-apple-darwin12-lipo \
	MACHOCHECK=x86_64-apple-darwin12-machocheck \
	NM=x86_64-apple-darwin12-nm \
	NMEDIT=x86_64-apple-darwin12-nmedit \
	OTOOL=x86_64-apple-darwin12-otool \
	PAGESTUFF=x86_64-apple-darwin12-pagestuff \
	PKG_CONFIG=x86_64-apple-darwin12-pkg-config \
	PKG_CONFIG_PATH=/opt/osxcross/macports/pkgs/opt/local/lib/pkgconfig \
	RANLIB=x86_64-apple-darwin12-ranlib \
	REDO_PREBINDING=x86_64-apple-darwin12-redo_prebinding \
	SEG_ADDR_TABLE=x86_64-apple-darwin12-seg_addr_table \
	SEG_HACK=x86_64-apple-darwin12-seg_hack \
	SEGEDIT=x86_64-apple-darwin12-segedit \
	SIZE=x86_64-apple-darwin12-size \
	STRINGS=x86_64-apple-darwin12-strings \
	STRIP=x86_64-apple-darwin12-strip \
	SW_VERS=x86_64-apple-darwin12-sw_vers \
	UNWINDDUMP=x86_64-apple-darwin12-unwinddump \
	WRAPPER=x86_64-apple-darwin12-wrapper

USER buildbot
WORKDIR /buildbot
