ARG DEFAULT_BASE_IMAGE
# TODO: Ask upstream to give us tags, since new devkitPro are frequently not
# backwards-compatible
FROM werner/devkitpro:latest as devkitpro
FROM ${DEFAULT_BASE_IMAGE} as libraries
ARG WORKER_NAME
USER root

COPY --from=devkitpro /opt/devkitpro/devkitARM /opt/devkitpro/devkitARM
COPY --from=devkitpro /opt/devkitpro/devkitPPC /opt/devkitpro/devkitPPC
COPY --from=devkitpro /opt/devkitpro/libctru /opt/devkitpro/libctru
COPY --from=devkitpro /opt/devkitpro/libgba /opt/devkitpro/libgba
COPY --from=devkitpro /opt/devkitpro/libmirko /opt/devkitpro/libmirko
COPY --from=devkitpro /opt/devkitpro/libnds /opt/devkitpro/libnds
COPY --from=devkitpro /opt/devkitpro/libogc /opt/devkitpro/libogc

# dpkg-dev is required to retrieve sources from apt
# libgmp10 is required by the ARM compiler
RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dpkg-dev \
		libgmp10

WORKDIR /tmp/compile
COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-nintendo.sh ./

# Library rules are copied separately along with their corresponding library
# so that changes or additions to individual library scripts don't invalidate
# every single library layer
COPY common/library-rules/zlib.sh library-rules/
RUN ./compile-libraries-nintendo.sh zlib

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-nintendo.sh libpng1.6

COPY common/library-rules/freetype.sh library-rules/
RUN ./compile-libraries-nintendo.sh freetype

COPY common/library-rules/libjpeg-turbo.sh library-rules/
RUN ./compile-libraries-nintendo.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-nintendo.sh faad2

COPY common/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-nintendo.sh libmad

RUN ./compile-libraries-nintendo.sh libogg

COPY common/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-nintendo.sh libtheora

COPY common/library-rules/libvorbisidec.sh library-rules/
RUN ./compile-libraries-nintendo.sh libvorbisidec

COPY common/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-nintendo.sh mpeg2dec

COPY ${WORKER_NAME}/library-rules/libgxflux.sh library-rules/
RUN ./compile-libraries-nintendo.sh libgxflux

# glibc       # configure fails, unsupported architecture
# flac        # build fails, utime/chown missing (from glibc)
# curl        # configure fails, gethostbyname missing (from glibc)
# glib2.0     # configure fails, iconv missing (from glibc)
# fluidsynth  # can't build, needs glib2.0
# libsdl2     # not used on this platform
# libsdl2-net # not used on this platform

FROM ${DEFAULT_BASE_IMAGE}
USER root

COPY --from=libraries /opt/devkitpro/devkitARM /opt/devkitpro/devkitARM
COPY --from=libraries /opt/devkitpro/devkitPPC /opt/devkitpro/devkitPPC
COPY --from=libraries /opt/devkitpro/libctru /opt/devkitpro/libctru
COPY --from=libraries /opt/devkitpro/libgba /opt/devkitpro/libgba
COPY --from=libraries /opt/devkitpro/libmirko /opt/devkitpro/libmirko
COPY --from=libraries /opt/devkitpro/libnds /opt/devkitpro/libnds
COPY --from=libraries /opt/devkitpro/libogc /opt/devkitpro/libogc
COPY --from=libraries /tmp/compile /tmp/compile

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		libgmp10 \
		&& \
	rm -rf /var/lib/apt/lists/*

ENV PATH=/opt/devkitpro/devkitARM/bin:/opt/devkitpro/devkitPPC/bin:$PATH
ENV DEVKITPRO=/opt/devkitpro
ENV DEVKITARM=$DEVKITPRO/devkitARM
ENV DEVKITPPC=$DEVKITPRO/devkitPPC

USER buildbot
WORKDIR /buildbot
