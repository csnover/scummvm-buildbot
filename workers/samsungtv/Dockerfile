ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE} AS compiler
USER root
ARG WORKER_NAME

WORKDIR /tmp/compile
# dpkg-dev is required to retrieve sources from apt
RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dpkg-dev \
		g++-arm-linux-gnueabi \
		gcc-arm-linux-gnueabi \
		pkg-config

WORKDIR /tmp/compile
COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-samsungtv.sh ./

COPY common/library-rules/zlib.sh library-rules/
RUN ./compile-libraries-samsungtv.sh zlib

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-samsungtv.sh libpng1.6

COPY common/library-rules/freetype.sh library-rules/
RUN ./compile-libraries-samsungtv.sh freetype

COPY common/library-rules/libjpeg-turbo.sh library-rules/
RUN ./compile-libraries-samsungtv.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-samsungtv.sh faad2

COPY common/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-samsungtv.sh libmad

RUN ./compile-libraries-samsungtv.sh libogg

COPY common/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-samsungtv.sh libtheora

RUN ./compile-libraries-samsungtv.sh libvorbis

RUN ./compile-libraries-samsungtv.sh curl

RUN ./compile-libraries-samsungtv.sh libsdl2

COPY common/library-rules/libsdl2-net.sh library-rules/
RUN ./compile-libraries-samsungtv.sh libsdl2-net

COPY ${WORKER_NAME}/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-samsungtv.sh mpeg2dec

# Using the 64-bit Debian image here just to reduce the number of layers with
# redundant data in them; DEFAULT_BASE_IMAGE would work fine too
FROM scummvm/buildbot-debian-x86_64:latest
USER root

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		g++-arm-linux-gnueabi \
		gcc-arm-linux-gnueabi \
		&& \
	rm -rf /var/lib/apt/lists/*

COPY --from=compiler /usr/arm-linux-gnueabi /usr/arm-linux-gnueabi

ENV PATH=$PATH:/usr/arm-linux-gnueabi/bin \
	ADDR2LINE=arm-linux-gnueabi-addr2line \
	AR=arm-linux-gnueabi-ar \
	AS=arm-linux-gnueabi-as \
	CXX=arm-linux-gnueabi-g++ \
	CXXFILT=arm-linux-gnueabi-c++filt \
	CPP=arm-linux-gnueabi-cpp \
	DWP=arm-linux-gnueabi-dwp \
	ELFEDIT=arm-linux-gnueabi-elfedit \
	GXX=arm-linux-gnueabi-g++ \
	GCC=arm-linux-gnueabi-gcc \
	GCOV=arm-linux-gnueabi-gcov \
	GCOV_DUMP=arm-linux-gnueabi-gcov-dump \
	GCOV_TOOL=arm-linux-gnueabi-gcov-tool \
	GPROF=arm-linux-gnueabi-gprof \
	LD=arm-linux-gnueabi-ld \
	NM=arm-linux-gnueabi-nm \
	OBJCOPY=arm-linux-gnueabi-objcopy \
	OBJDUMP=arm-linux-gnueabi-objdump \
	RANLIB=arm-linux-gnueabi-ranlib \
	READELF=arm-linux-gnueabi-readelf \
	SIZE=arm-linux-gnueabi-size \
	STRINGS=arm-linux-gnueabi-strings \
	STRIP=arm-linux-gnueabi-strip

USER buildbot
WORKDIR /buildbot
