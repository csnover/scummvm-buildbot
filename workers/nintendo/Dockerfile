ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM werner/devkitpro@sha256:c5c6762b55c444fcd2c8b3d7265b11922e5b7885451bdd2a9d25c6d953d434b2 as devkitpro
FROM ${DEFAULT_OS_IMAGE} as libraries
USER root
ARG WORKER_NAME

COPY --from=devkitpro /opt/devkitpro/devkitPPC /opt/devkitpro/devkitPPC
COPY --from=devkitpro /opt/devkitpro/libogc /opt/devkitpro/libogc

ENV DEVKITPRO=/opt/devkitpro
ENV DEVKITPPC=$DEVKITPRO/devkitPPC
ENV PATH=$PATH:$DEVKITPPC/bin

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

COPY common/library-rules/libjpeg-turbo-no-simd.sh library-rules/libjpeg-turbo.sh
RUN ./compile-libraries-nintendo.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-nintendo.sh faad2

COPY common/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-nintendo.sh libmad

COPY common/library-rules/libogg.sh library-rules/
RUN ./compile-libraries-nintendo.sh libogg

COPY common/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-nintendo.sh libtheora

COPY common/library-rules/libvorbisidec.sh library-rules/
RUN ./compile-libraries-nintendo.sh libvorbisidec

COPY ${WORKER_NAME}/library-rules/flac.sh library-rules/
RUN ./compile-libraries-nintendo.sh flac

COPY common/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-nintendo.sh mpeg2dec

COPY ${WORKER_NAME}/library-rules/libgxflux.sh library-rules/
RUN ./compile-libraries-nintendo.sh libgxflux

# glibc       # configure fails, unsupported architecture
# curl        # configure fails, gethostbyname missing (from glibc)
# glib2.0     # configure fails, iconv missing (from glibc)
# fluidsynth  # can't build, needs glib2.0
# libsdl2     # not used on this platform
# libsdl2-net # not used on this platform

FROM ${DEFAULT_BASE_IMAGE}
USER root

COPY --from=libraries /opt/devkitpro/devkitPPC /opt/devkitpro/devkitPPC
COPY --from=libraries /opt/devkitpro/libogc /opt/devkitpro/libogc

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		libgmp10 \
		&& \
	rm -rf /var/lib/apt/lists/*

ENV DEVKITPRO=/opt/devkitpro
ENV DEVKITPPC=$DEVKITPRO/devkitPPC
ENV PATH=$PATH:$DEVKITPPC/bin:$DEVKITPPC/powerpc-eabi/bin

USER buildbot
WORKDIR /buildbot
