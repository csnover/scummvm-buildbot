ARG DEFAULT_BASE_IMAGE
FROM werner/devkitpro:latest as devkitpro
FROM ${DEFAULT_BASE_IMAGE} as libraries

COPY --from=devkitpro /opt/devkitpro/devkitARM /opt/devkitpro/devkitARM
COPY --from=devkitpro /opt/devkitpro/devkitPPC /opt/devkitpro/devkitPPC
COPY --from=devkitpro /opt/devkitpro/libctru /opt/devkitpro/libctru
COPY --from=devkitpro /opt/devkitpro/libgba /opt/devkitpro/libgba
COPY --from=devkitpro /opt/devkitpro/libmirko /opt/devkitpro/libmirko
COPY --from=devkitpro /opt/devkitpro/libnds /opt/devkitpro/libnds
COPY --from=devkitpro /opt/devkitpro/libogc /opt/devkitpro/libogc

# dpkg-dev   # required to retrieve sources from apt
# libgmp10   # required by the ARM compiler
# debhelper  # required by libmad
# quilt      # required by libmad
# pkg-config # required by fluidsynth
RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
	> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		debhelper \
		dpkg-dev \
		libgmp10 \
		pkg-config \
		quilt

WORKDIR /tmp/compile
COPY compile-libraries.sh .
RUN ./compile-libraries.sh zlib libpng1.6 freetype
RUN ./compile-libraries.sh libjpeg-turbo
RUN ./compile-libraries.sh faad2
RUN ./compile-libraries.sh libmad
RUN ./compile-libraries.sh libogg libtheora libvorbisidec
RUN ./compile-libraries.sh mpeg2dec
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
