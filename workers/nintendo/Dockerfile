ARG DEFAULT_BASE_IMAGE
FROM werner/devkitpro:559a46fa7958 as devkitpro
FROM ${DEFAULT_BASE_IMAGE} as libraries

COPY --from=devkitpro /opt/devkitpro/devkitARM /opt/devkitpro/devkitARM
COPY --from=devkitpro /opt/devkitpro/devkitPPC /opt/devkitpro/devkitPPC
COPY --from=devkitpro /opt/devkitpro/libctru /opt/devkitpro/libctru
COPY --from=devkitpro /opt/devkitpro/libgba /opt/devkitpro/libgba
COPY --from=devkitpro /opt/devkitpro/libmirko /opt/devkitpro/libmirko
COPY --from=devkitpro /opt/devkitpro/libnds /opt/devkitpro/libnds
COPY --from=devkitpro /opt/devkitpro/libogc /opt/devkitpro/libogc

# ca-certificates # required to retrieve libgxflux
# dpkg-dev        # required to retrieve sources from apt
# libgmp10        # required by the ARM compiler
# debhelper       # required by libmad
# quilt           # required by libmad
# pkg-config      # required by fluidsynth
# wget            # required to retrieve libgxflux
RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
	> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		debhelper \
		dpkg-dev \
		git \
		libgmp10 \
		pkg-config \
		quilt \
		wget

WORKDIR /tmp/compile
COPY compile-libraries.sh .

# Library rules are copied separately along with their corresponding library
# so that changes or additions to individual library scripts don't invalidate
# every single library layer
COPY library-rules/zlib.sh library-rules/libpng1.6.sh library-rules/freetype.sh library-rules/
RUN ./compile-libraries.sh zlib libpng1.6 freetype

COPY library-rules/libjpeg-turbo.sh library-rules/
RUN ./compile-libraries.sh libjpeg-turbo

COPY library-rules/faad2.sh library-rules/
RUN ./compile-libraries.sh faad2

COPY library-rules/libmad.sh library-rules/
RUN ./compile-libraries.sh libmad

COPY library-rules/libtheora.sh library-rules/libvorbisidec.sh library-rules/
RUN ./compile-libraries.sh libogg libtheora libvorbisidec

COPY library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries.sh mpeg2dec

COPY library-rules/libgxflux.sh library-rules/
RUN ./compile-libraries.sh libgxflux

# glibc       # configure fails, unsupported architecture
# flac        # build fails, utime/chown missing (from glibc)
# curl        # configure fails, gethostbyname missing (from glibc)
# glib2.0     # configure fails, iconv missing (from glibc)
# fluidsynth  # can't build, needs glib2.0
# libsdl2     # not used on this platform
# libsdl2-net # not used on this platform

FROM ${DEFAULT_BASE_IMAGE}

ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}

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
		ccache \
		dumb-init \
		git \
		gzip \
		libgmp10 \
		make \
		python-openssl \
		python-pip \
		python-twisted \
		rsync \
		xz-utils \
		&& \
	rm -rf /var/lib/apt/lists/*

RUN pip --no-cache-dir install \
		buildbot-worker==${BUILDBOT_VERSION}

ENV PATH=/opt/devkitpro/devkitARM/bin:/opt/devkitpro/devkitPPC/bin:$PATH
ENV DEVKITPRO=/opt/devkitpro
ENV DEVKITARM=$DEVKITPRO/devkitARM
ENV DEVKITPPC=$DEVKITPRO/devkitPPC

RUN useradd -ms /bin/bash -d /buildbot -u 2845 -U buildbot
RUN mkdir -p /data/sharedrepo && chown buildbot:buildbot /data/sharedrepo

USER buildbot
WORKDIR /buildbot
COPY buildbot.tac /buildbot
CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
