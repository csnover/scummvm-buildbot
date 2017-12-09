ARG DEFAULT_BASE_IMAGE
FROM debian:8 AS compiler
ARG WORKER_NAME
COPY ${WORKER_NAME}/diablo-toolchain.list /etc/apt/sources.list.d/
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends --force-yes \
	diablo-gcc-5 \
	diablo-package-tools \
	&& rm -rf /var/lib/apt/lists/*
RUN /opt/diablo/bin/apt-get update && \
	DEBIAN_FRONTEND=noninteractive /opt/diablo/bin/apt-get -y --no-install-recommends --force-yes install \
		libsdl1.2-dev \
		libpng12-dev \
		libjpeg62-dev \
		libfreetype6-dev \
		libflac-dev \
		libmad0-dev \
		libmpeg2-4-dev \
		libvorbisidec-dev && \
	rm -rf /opt/diablo/root/var/lib/apt/lists/*

FROM ${DEFAULT_BASE_IMAGE}
USER root
COPY --from=compiler /opt/diablo /opt/diablo

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		libmpc3 && \
	rm -rf /var/lib/apt/lists/*

ENV PATH=$PATH:/opt/diablo/root/usr/bin:/opt/diablo/gcc-5/bin \
	ADDR2LINE=arm-none-linux-gnueabi-addr2line \
	AR=arm-none-linux-gnueabi-ar \
	AS=arm-none-linux-gnueabi-as \
	CXX=arm-none-linux-gnueabi-c++ \
	CXXFILT=arm-none-linux-gnueabi-c++filt \
	CPP=arm-none-linux-gnueabi-cpp \
	ELFEDIT=arm-none-linux-gnueabi-elfedit \
	GXX=arm-none-linux-gnueabi-g++ \
	GCC=arm-none-linux-gnueabi-gcc \
	GCOV=arm-none-linux-gnueabi-gcov \
	GCOV_TOOL=arm-none-linux-gnueabi-gcov-tool \
	GPROF=arm-none-linux-gnueabi-gprof \
	LD=arm-none-linux-gnueabi-ld \
	NM=arm-none-linux-gnueabi-nm \
	OBJCOPY=arm-none-linux-gnueabi-objcopy \
	OBJDUMP=arm-none-linux-gnueabi-objdump \
	RANLIB=arm-none-linux-gnueabi-ranlib \
	READELF=arm-none-linux-gnueabi-readelf \
	SIZE=arm-none-linux-gnueabi-size \
	STRINGS=arm-none-linux-gnueabi-strings \
	STRIP=arm-none-linux-gnueabi-strip

USER buildbot
WORKDIR /buildbot
