ARG DEFAULT_BASE_IMAGE
FROM ubuntu:12.04 AS pspdev
ARG WORKER_NAME

ENV TOOLCHAIN_VERSION 665124fc2820ac532dc06e38b8118fd35e713537

ENV PSPDEV /pspdev
ENV PSPSDK $PSPDEV/psp
ENV PATH   $PATH:$PSPDEV/bin:$PSPSDK/bin

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		g++ \
		build-essential \
		autoconf \
		automake \
		cmake \
		doxygen \
		bison \
		flex \
		libncurses5-dev \
		libsdl1.2-dev \
		libreadline-dev \
		libusb-dev \
		texinfo \
		libgmp3-dev \
		libmpfr-dev \
		libelf-dev \
		libmpc-dev \
		libfreetype6-dev \
		zlib1g-dev \
		libtool \
		subversion \
		git \
		tcl \
		unzip \
		wget && \
	echo "dash dash/sh boolean false" | debconf-set-selections && \
	dpkg-reconfigure --frontend=noninteractive dash && \
	rm -rf /var/lib/apt/lists/*
COPY ${WORKER_NAME}/set-e.patch \
	${WORKER_NAME}/https.patch \
	${WORKER_NAME}/fix-soft-float.patch \
	../
ARG TOOLCHAIN_VERSION=665124fc2820ac532dc06e38b8118fd35e713537
RUN wget --progress=bar:force:noscroll -O - \
		https://github.com/pspdev/psptoolchain/archive/${TOOLCHAIN_VERSION}.tar.gz | \
		tar --strip-components=1 -zxf - && \
	patch -p1 < ../set-e.patch && \
	patch -p1 < ../https.patch && \
	patch -p1 < ../fix-soft-float.patch
RUN ./toolchain.sh

FROM ${DEFAULT_BASE_IMAGE}
COPY --from=pspdev /pspdev /pspdev
USER root
# In at least Docker 17.09 these ENV commands need to be separate since
# otherwise references to $PSPDEV and $PSPSDK will be missing
ENV PSPDEV /pspdev
ENV PSPSDK $PSPDEV/psp
ENV PATH=$PATH:$PSPDEV/bin:$PSPSDK/bin \
	CXXFLAGS="$CXXFLAGS -isystem /pspdev/psp/sdk/include" \
	LDFLAGS="$LDFLAGS -L /pspdev/psp/sdk/lib" \
	ADDR2LINE=psp-addr2line \
	AR=psp-ar \
	AS=psp-as \
	CXX=psp-c++ \
	CXXFILT=psp-c++filt \
	CMAKE=psp-cmake \
	CPP=psp-cpp \
	ELFEDIT=psp-elfedit \
	GXX=psp-g++ \
	GCC=psp-gcc \
	GCOV=psp-gcov \
	GDB=psp-gdb \
	LD=psp-ld \
	NM=psp-nm \
	OBJCOPY=psp-objcopy \
	OBJDUMP=psp-objdump \
	RANLIB=psp-ranlib \
	READELF=psp-readelf \
	SIZE=psp-size \
	STRINGS=psp-strings \
	STRIP=psp-strip

USER buildbot
WORKDIR /buildbot
