ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE} as compilers
USER root
ARG WORKER_NAME

RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		automake \
		build-essential \
		ca-certificates \
		clang \
		cmake \
		dpkg-dev \
		git \
		gobjc \
		gzip \
		libssl-dev \
		libtool \
		patch \
		pkg-config \
		python \
		xz-utils

WORKDIR /tmp
COPY ${WORKER_NAME}/build-ios.sh.patch build-ios.sh.patch
COPY ${WORKER_NAME}/iPhoneOS7.1.sdk.tar.gz .

WORKDIR /tmp/compile
RUN git clone https://github.com/tpoechtrager/cctools-port.git . && \
	git checkout c1cc75893ed1978174fdcd1b898f81e6535e82d3 && \
	cd usage_examples/ios_toolchain && \
	patch -p1 < /tmp/build-ios.sh.patch && \
	./build.sh /tmp/iPhoneOS7.1.sdk.tar.gz armv7 && \
	mv target /opt/ioscross/ && \
	rm -rf /tmp/compile

RUN mv /opt/ioscross/lib/libtapi.so /opt/ioscross/bin
ENV LD_LIBRARY_PATH=/opt/ioscross/bin \
	PATH=$PATH:/opt/ioscross/bin \
	CFLAGS="$CFLAGS -arch armv7" \
	CXXFLAGS="$CXXFLAGS -arch armv7" \
	LDFLAGS="$LDFLAGS -arch armv7"

WORKDIR /tmp/compile
COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-ios.sh ./

# Library rules are copied separately along with their corresponding library
# so that changes or additions to individual library scripts don't invalidate
# every single library layer
COPY common/library-rules/zlib.sh library-rules/
RUN ./compile-libraries-ios.sh zlib

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-ios.sh libpng1.6

COPY common/library-rules/freetype.sh library-rules/
RUN ./compile-libraries-ios.sh freetype

COPY common/library-rules/libjpeg-turbo-no-simd.sh library-rules/libjpeg-turbo.sh
RUN ./compile-libraries-ios.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-ios.sh faad2

COPY common/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-ios.sh libmad

COPY common/library-rules/libogg.sh library-rules/
RUN ./compile-libraries-ios.sh libogg

COPY common/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-ios.sh libtheora

COPY common/library-rules/libvorbis.sh library-rules/
RUN ./compile-libraries-ios.sh libvorbis

COPY common/library-rules/flac.sh library-rules/
RUN ./compile-libraries-ios.sh flac

COPY ${WORKER_NAME}/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-ios.sh mpeg2dec

# Cribbing from macOS here since the underlying OS kernel is the same so the
# patchset is the same
COPY macos/library-rules/fluidsynth-lite.sh library-rules/
COPY macos/fluidsynth-lite-macos.patch ./
RUN ./compile-libraries-ios.sh fluidsynth-lite

COPY ${WORKER_NAME}/library-rules/curl.sh library-rules/
COPY ${WORKER_NAME}/curl-ios.patch .
# cURL will not enable DarwinSSL unless it finds the security framework in the
# root of the disk. Also, cURL acinclude.m4 will try to add
# -mmacosx-version-min=10.8 if it does not see anything in $CFLAGS matching
# m.*os.*-version-min. The ioscross compiler wrapper adds
# -miphoneos-version-min=7.1 later, and the two are not compatible so this
# causes a compilation error during configuration. Adding the flag
# explicitly fixes configuration by stopping cURL from adding its flag.
RUN ln -s /opt/ioscross/SDK/iPhoneOS7.1.sdk/System /System && \
	CFLAGS=-miphoneos-version-min=7.1 ./compile-libraries-ios.sh curl && \
	rm /System && \
	sed -i \
		-e 's/-Wl,-Bstatic//' \
		-e 's/-Wl,-Bdynamic//' \
		/opt/ioscross/bin/curl-config

FROM ${DEFAULT_BASE_IMAGE}
USER root
ARG WORKER_NAME

COPY --from=compilers /opt/ioscross /opt/ioscross

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		clang \
		llvm-dev \
		uuid-dev \
		&& \
	rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/opt/ioscross/bin:$LD_LIBRARY_PATH \
	PATH=$PATH:/opt/ioscross/bin \
	CFLAGS="$CFLAGS -arch armv7 -isystem /opt/ioscross/include" \
	CXXFLAGS="$CXXFLAGS -arch armv7 -isystem /opt/ioscross/include" \
	LDFLAGS="$LDFLAGS -arch armv7 -L/opt/ioscross/lib" \
	OBJECTDUMP=arm-apple-darwin11-ObjectDump \
	AR=arm-apple-darwin11-ar \
	AS=arm-apple-darwin11-as \
	BITCODE_STRIP=arm-apple-darwin11-bitcode_strip \
	CXX=arm-apple-darwin11-clang++ \
	CC=arm-apple-darwin11-clang \
	CHECK_DYLIB=arm-apple-darwin11-check_dylib \
	CHECKSYMS=arm-apple-darwin11-checksyms \
	CMPDYLIB=arm-apple-darwin11-cmpdylib \
	CODESIGN_ALLOCATE=arm-apple-darwin11-codesign_allocate \
	CTF_INSERT=arm-apple-darwin11-ctf_insert \
	DYLDINFO=arm-apple-darwin11-dyldinfo \
	INDR=arm-apple-darwin11-indr \
	INOUT=arm-apple-darwin11-inout \
	INSTALL_NAME_TOOL=arm-apple-darwin11-install_name_tool \
	LD=arm-apple-darwin11-ld \
	LIBTOOL=arm-apple-darwin11-libtool \
	LIPO=arm-apple-darwin11-lipo \
	MACHOCHECK=arm-apple-darwin11-machocheck \
	NM=arm-apple-darwin11-nm \
	NMEDIT=arm-apple-darwin11-nmedit \
	OTOOL=arm-apple-darwin11-otool \
	PAGESTUFF=arm-apple-darwin11-pagestuff \
	PKG_CONFIG=arm-apple-darwin11-pkg-config \
	PKG_CONFIG_PATH=/opt/ioscross/lib/pkgconfig \
	RANLIB=arm-apple-darwin11-ranlib \
	REDO_PREBINDING=arm-apple-darwin11-redo_prebinding \
	SEG_ADDR_TABLE=arm-apple-darwin11-seg_addr_table \
	SEG_HACK=arm-apple-darwin11-seg_hack \
	SEGEDIT=arm-apple-darwin11-segedit \
	SIZE=arm-apple-darwin11-size \
	STRINGS=arm-apple-darwin11-strings \
	STRIP=arm-apple-darwin11-strip \
	UNWINDDUMP=arm-apple-darwin11-unwinddump

USER buildbot
WORKDIR /buildbot
