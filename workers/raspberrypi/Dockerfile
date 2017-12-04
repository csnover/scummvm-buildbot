ARG DEFAULT_BASE_IMAGE
FROM sdthirlwall/raspberry-pi-cross-compiler@sha256:f14f0bd23e766ed40ec109d9fe98aab68229b5ccce1d4acde09327549e1588d7 AS compiler
LABEL maintainer="ScummVM Team <admin@scummvm.org>"
USER root
ARG WORKER_NAME

RUN rpdo apt-get update && install-raspbian -y --no-install-recommends \
		libsdl2-dev \
		libpng12-dev \
		zlib1g-dev \
		libfaad-dev \
		libflac-dev \
		libmad0-dev \
		libjpeg62-turbo-dev \
		libfreetype6-dev \
		libfluidsynth-dev \
		libvorbisidec-dev \
		libvorbis-dev \
		libtheora-dev \
		libmpeg2-4-dev \
		libcurl4-openssl-dev \
		libsdl2-net-dev && \
	rpdo rm -rf /var/lib/apt/lists/*

FROM ${DEFAULT_BASE_IMAGE}
USER root
COPY --from=compiler /rpxc /rpxc

ENV PATH=$PATH:/rpxc/bin:/rpxc/sysroot/usr/bin \
	CXXFLAGS="$CXXFLAGS --sysroot=/rpxc/sysroot" \
	LDFLAGS="$LDFLAGS --sysroot=/rpxc/sysroot" \
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

# ScummVM configure-specific
ENV RPI_ROOT=/rpxc/sysroot

USER buildbot
WORKDIR /buildbot
