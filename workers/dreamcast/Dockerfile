ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE} AS compiler
USER root
ARG WORKER_NAME

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		build-essential \
		bzip2 \
		ca-certificates \
		file \
		libcloog-isl-dev \
		libisl-dev \
		libmpc-dev \
		libmpfr-dev \
		texinfo \
		wget \
		zlib1g-dev \
		&& \
	rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/compile
ARG GCC_VER=7.1.0
RUN wget --progress=bar:force:noscroll -O - \
		https://ftp.gnu.org/gnu/gcc/gcc-$GCC_VER/gcc-$GCC_VER.tar.gz \
		| tar zxf -
ARG BINUTILS_VER=2.25
RUN wget --progress=bar:force:noscroll -O - \
		https://ftp.gnu.org/gnu/binutils/binutils-$BINUTILS_VER.tar.gz \
		| tar zxf -
ARG NEWLIB_VER=2.2.0
RUN wget --progress=bar:force:noscroll -O - \
		https://sourceware.org/pub/newlib/newlib-$NEWLIB_VER.tar.gz \
		| tar zxf -
# Downloading GCC dependencies manually because the contrib script for
# retrieving dependencies *still* uses FTP
ARG GMP_VER=6.1.0
RUN mkdir gcc-$GCC_VER/gmp && \
	wget --progress=bar:force:noscroll -O - \
		https://ftp.gnu.org/gnu/gmp/gmp-$GMP_VER.tar.xz \
		| tar --strip-components=1 -C gcc-$GCC_VER/gmp -xJf -
ARG MPFR_VER=3.1.4
RUN mkdir gcc-$GCC_VER/mpfr && \
	wget --progress=bar:force:noscroll -O - \
		https://ftp.gnu.org/gnu/mpfr/mpfr-$MPFR_VER.tar.gz \
		| tar --strip-components=1 -C gcc-$GCC_VER/mpfr -zxf -
ARG MPC_VER=1.0.3
RUN mkdir gcc-$GCC_VER/mpc && \
	wget --progress=bar:force:noscroll -O - \
		https://ftp.gnu.org/gnu/mpc/mpc-$MPC_VER.tar.gz \
		| tar --strip-components=1 -C gcc-$GCC_VER/mpc -zxf -
ARG ISL_VER=0.16.1
RUN mkdir gcc-$GCC_VER/isl && \
	wget --progress=bar:force:noscroll -O - \
		https://gcc.gnu.org/pub/gcc/infrastructure/isl-0.16.1.tar.bz2 \
		| tar --strip-components=1 -C gcc-$GCC_VER/mpc -xjf -

ENV PATH=$PATH:/opt/dc/bin

# SH
WORKDIR /tmp/compile/build
RUN ../binutils-$BINUTILS_VER/configure \
		--prefix=/opt/dc \
		--target=sh-elf \
		--disable-werror && \
	make -j$(nproc) && \
	make -j$(nproc) install && \
	rm -r ../build

WORKDIR /tmp/compile/build
RUN ../gcc-$GCC_VER/configure \
		--prefix=/opt/dc \
		--build=$(dpkg-architecture -qDEB_BUILD_GNU_TYPE) \
		--host=$(dpkg-architecture -qDEB_HOST_GNU_TYPE) \
		--target=sh-elf \
		--enable-languages=c \
		--disable-nls \
		--disable-tls \
		--disable-libssp \
		--disable-werror \
		--without-headers \
		--with-newlib \
		--with-multilib-list=m4-single-only,m4-nofpu,m4 \
		--with-endian=little \
		--with-cpu=m4-single-only && \
	make -j$(nproc) && \
	make -j$(nproc) install && \
	rm -r ../build

WORKDIR /tmp/compile/build
RUN ../newlib-$NEWLIB_VER/configure \
		--prefix=/opt/dc \
		--build=$(dpkg-architecture -qDEB_BUILD_GNU_TYPE) \
		--host=$(dpkg-architecture -qDEB_HOST_GNU_TYPE) \
		--target=sh-elf \
		--with-multilib-list=m4-single-only,m4-nofpu,m4 \
		--with-endian=little \
		--with-cpu=m4-single-only && \
	make -j$(nproc) && \
	make -j$(nproc) install && \
	rm -r ../build

WORKDIR /tmp/compile/build
RUN ../gcc-$GCC_VER/configure \
		--prefix=/opt/dc \
		--build=$(dpkg-architecture -qDEB_BUILD_GNU_TYPE) \
		--host=$(dpkg-architecture -qDEB_HOST_GNU_TYPE) \
		--target=sh-elf \
		--enable-languages=c,c++ \
		--disable-nls \
		--disable-tls \
		--disable-libssp \
		--disable-werror \
		--with-newlib \
		--with-multilib-list=m4-single-only,m4-nofpu,m4 \
		--with-endian=little \
		--with-cpu=m4-single-only && \
	make -j$(nproc) && \
	make -j$(nproc) install && \
	rm -r ../build

# ARM
WORKDIR /tmp/compile/build
RUN ../binutils-$BINUTILS_VER/configure \
		--prefix=/opt/dc \
		--target=arm-none-eabi \
		--disable-werror && \
	make -j$(nproc) && \
	make -j$(nproc) install && \
	rm -r ../build

WORKDIR /tmp/compile/build
RUN ../gcc-$GCC_VER/configure \
		--prefix=/opt/dc \
		--build=$(dpkg-architecture -qDEB_BUILD_GNU_TYPE) \
		--host=$(dpkg-architecture -qDEB_HOST_GNU_TYPE) \
		--target=arm-none-eabi \
		--enable-languages=c \
		--disable-nls \
		--disable-tls \
		--disable-libssp \
		--disable-libgcc \
		--disable-werror \
		--disable-multilib \
		--without-headers \
		--with-newlib \
		--with-mode=arm \
		# The ARM coprocessor is actually an armv3 part, but portions of newlib
		# (e.g. strcmp) use armv4-specific instructions which are not likely to
		# ever actually be executed, so just use armv4 even though it is a bit
		# wrong
		--with-arch=armv4 && \
	make -j$(nproc) && \
	make -j$(nproc) install && \
	rm -r ../build

WORKDIR /tmp/compile/build
RUN ../newlib-$NEWLIB_VER/configure \
		--prefix=/opt/dc \
		--build=$(dpkg-architecture -qDEB_BUILD_GNU_TYPE) \
		--host=$(dpkg-architecture -qDEB_HOST_GNU_TYPE) \
		--target=arm-none-eabi \
		--enable-newlib-hw-fp && \
	make -j$(nproc) && \
	make -j$(nproc) install && \
	rm -r ../build

WORKDIR /tmp/compile/build
RUN ../gcc-$GCC_VER/configure \
		--prefix=/opt/dc \
		--build=$(dpkg-architecture -qDEB_BUILD_GNU_TYPE) \
		--host=$(dpkg-architecture -qDEB_HOST_GNU_TYPE) \
		--target=arm-none-eabi \
		--enable-languages=c,c++ \
		--disable-nls \
		--disable-tls \
		--disable-libssp \
		--disable-werror \
		--without-headers \
		--with-newlib \
		--with-arch=armv4 && \
	make -j$(nproc) && \
	make -j$(nproc) install && \
	rm -r ../build

WORKDIR /tmp/compile
COPY ${WORKER_NAME}/ronin-notlibc.patch .
RUN apt-get update && apt-get install -y --no-install-recommends \
	p7zip-full \
	pike8.0-core
RUN wget --progress=bar:force:noscroll -O libronin.7z \
		https://sourceforge.net/projects/dcevolution/files/Programming/dcevo-DCDev-Libronin-0.6-source.7z/download && \
	p7zip -d -c libronin.7z | tar xf - && \
	rm libronin.7z && \
	cd ronin-src && \
	patch -p1 < ../ronin-notlibc.patch && \
	sed -e 's/arm-elf-/arm-none-eabi-/g' \
		-e 's/-marm7/-mcpu=arm7/g' \
		-i Makefile && \
	sed -e 's/ asm / __asm__ /g' -i lwip/arch/dc/sys_arch.c && \
	sed -e 's/asm(/__asm__(/g' -i ta.c c_video.c && \
	sed -e 's/itoa/ronin_itoa/g' -i report.c report.h vmsfs.c && \
	# This makefile has bad dependency management and breaks if it has more than
	# one job
	make dist && \
	tar -C /opt/dc -xf ronin-dist.tar.gz

COPY ${WORKER_NAME}/source/ ./
RUN gcc -o /opt/dc/bin/scramble scramble.c && \
	gcc -o /opt/dc/bin/makeip makeip.c && \
	gcc -o /opt/dc/bin/selfbootnrg selfbootnrg.c

COPY ${WORKER_NAME}/IP.TMPL /opt/dc/bin/

COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-dreamcast.sh ./

RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dpkg-dev \
		pkg-config

# Use ronin's zlib
ENV CPPFLAGS="-isystem /opt/dc/ronin/include" \
	LDFLAGS="$LDFLAGS -L/opt/dc/ronin/lib"

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-dreamcast.sh libpng1.6

COPY common/library-rules/libjpeg-turbo.sh library-rules/
RUN ./compile-libraries-dreamcast.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-dreamcast.sh faad2

COPY common/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-dreamcast.sh libmad

COPY common/library-rules/libogg.sh library-rules/
RUN ./compile-libraries-dreamcast.sh libogg

COPY common/library-rules/libvorbisidec.sh library-rules/
RUN ./compile-libraries-dreamcast.sh libvorbisidec

FROM ${DEFAULT_BASE_IMAGE}
USER root
COPY --from=compiler /opt/dc /opt/dc
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y \
		libisl15 \
		libmpc3 \
		&& \
	rm -rf /var/lib/apt/lists/*
ENV PATH=$PATH:/opt/dc/bin \
	RONINDIR=/opt/dc/ronin \
	IP_TEMPLATE_FILE=/opt/dc/bin/IP.TMPL \
	CXXFLAGS="$CXXFLAGS -isystem /opt/dc/ronin/include" \
	LDFLAGS="$LDFLAGS -L/opt/dc/ronin/lib"
USER buildbot
WORKDIR /buildbot
