ARG DEFAULT_BASE_IMAGE
FROM ${DEFAULT_BASE_IMAGE}
USER root

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		clang \
		g++ \
		libcurl4-openssl-dev \
		libfaad-dev \
		libflac-dev \
		libfluidsynth-dev \
		libfreetype6-dev \
		libjpeg62-turbo-dev \
		libmad0-dev \
		libmpeg2-4-dev \
		libpng-dev \
		libsdl2-dev \
		libsdl2-net-dev \
		libtheora-dev \
		libvorbis-dev \
		zlib1g-dev \
		&& \
	rm -rf /var/lib/apt/lists/*

USER buildbot
WORKDIR /buildbot
