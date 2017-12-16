ARG DEFAULT_BASE_IMAGE
FROM ${DEFAULT_BASE_IMAGE}
USER root

RUN dpkg --add-architecture armhf && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		g++-arm-linux-gnueabihf \
		libcurl4-openssl-dev:armhf \
		libfaad-dev:armhf \
		libflac-dev:armhf \
		libfluidsynth-dev:armhf \
		libfreetype6-dev:armhf \
		libjpeg62-turbo-dev:armhf \
		libmad0-dev:armhf \
		libmpeg2-4-dev:armhf \
		libpng-dev:armhf \
		libsdl2-dev:armhf \
		libsdl2-net-dev:armhf \
		libtheora-dev:armhf \
		libvorbis-dev:armhf \
		zlib1g-dev:armhf \
		&& \
	rm -rf /var/lib/apt/lists/*

USER buildbot
WORKDIR /buildbot

ENV PATH=$PATH:/usr/arm-linux-gnueabihf/bin \
	ADDR2LINE=arm-linux-gnueabihf-addr2line \
	AR=arm-linux-gnueabihf-ar \
	AS=arm-linux-gnueabihf-as \
	CXX=arm-linux-gnueabihf-g++ \
	CXXFILT=arm-linux-gnueabihf-c++filt \
	CPP=arm-linux-gnueabihf-cpp \
	DWP=arm-linux-gnueabihf-dwp \
	ELFEDIT=arm-linux-gnueabihf-elfedit \
	GXX=arm-linux-gnueabihf-g++ \
	GCC=arm-linux-gnueabihf-gcc \
	GCOV=arm-linux-gnueabihf-gcov \
	GDB=arm-linux-gnueabihf-gdb \
	GFORTRAN=arm-linux-gnueabihf-gfortran \
	GPROF=arm-linux-gnueabihf-gprof \
	LD=arm-linux-gnueabihf-ld.gold \
	LDD=arm-linux-gnueabihf-ldd \
	NM=arm-linux-gnueabihf-nm \
	OBJCOPY=arm-linux-gnueabihf-objcopy \
	OBJDUMP=arm-linux-gnueabihf-objdump \
	PKG_CONFIG=arm-linux-gnueabihf-pkg-config \
	RANLIB=arm-linux-gnueabihf-ranlib \
	READELF=arm-linux-gnueabihf-readelf \
	SIZE=arm-linux-gnueabihf-size \
	STRINGS=arm-linux-gnueabihf-strings \
	STRIP=arm-linux-gnueabihf-strip

USER buildbot
WORKDIR /buildbot
