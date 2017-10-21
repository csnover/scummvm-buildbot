ARG DEFAULT_BASE_IMAGE
FROM ${DEFAULT_BASE_IMAGE}
USER root

RUN dpkg --add-architecture i386 && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		clang \
		g++ \
		g++-multilib \
		g++-mingw-w64 \
		libcurl4-openssl-dev \
		libcurl3:i386 \
		libfaad-dev \
		libfaad-dev:i386 \
		libflac-dev \
		libflac-dev:i386 \
		libfluidsynth-dev \
		libfluidsynth1:i386 \
		libfreetype6-dev \
		libfreetype6:i386 \
		libjpeg62-turbo-dev \
		libjpeg62-turbo-dev:i386 \
		libmad0-dev \
		libmad0:i386 \
		libmpeg2-4-dev \
		libmpeg2-4-dev:i386 \
		libpng-dev \
		libpng-dev:i386 \
		libsdl2-dev \
		libsdl2-2.0-0:i386 \
		libsdl2-net-dev \
		libsdl2-net-2.0-0:i386 \
		libtheora-dev \
		libtheora-dev:i386 \
		libvorbis-dev \
		libvorbis-dev:i386 \
		zlib1g-dev \
		zlib1g-dev:i386 \
		&& \
	rm -rf /var/lib/apt/lists/*

# HACK: multi-arch jessie packages for SDL cannot be installed side-by-side
# because of an architecture conflict in its dependencies, so just extract
# their libs so we can still link
WORKDIR /tmp
RUN apt-get update && \
	apt-get download libsdl2-dev:i386 libsdl2-net-dev:i386 && \
	dpkg --fsys-tarfile libsdl2-dev_*_i386.deb |tar --wildcards -C / -xf - './usr/lib/i386-linux-gnu/*' && \
	dpkg --fsys-tarfile libsdl2-net-dev_*_i386.deb |tar --wildcards -C / -xf - './usr/lib/i386-linux-gnu/*' && \
	rm libsdl2*.deb && \
	rm -rf /var/lib/apt/lists/* && \
	apt-get clean

USER buildbot
WORKDIR /buildbot
