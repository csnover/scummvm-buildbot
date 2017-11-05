ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE} AS compiler
USER root
ARG WORKER_NAME

WORKDIR /tmp/compile
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		dirmngr \
		gnupg \
		wget \
		&& \
	apt-key adv \
		--keyserver hkp://keyserver.ubuntu.com:80 \
		--recv-keys BFD8768B6878C33FDFD082C94AAD3A5DB5690522 && \
	echo 'deb http://ppa.launchpad.net/vriviere/ppa/ubuntu zesty main' \
		> /etc/apt/sources.list.d/freemint.list && \
	echo 'deb-src http://ppa.launchpad.net/vriviere/ppa/ubuntu zesty main' \
		>> /etc/apt/sources.list.d/freemint.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		binutils-m68k-atari-mint && \
	DEBIAN_FRONTEND=noninteractive apt-get build-dep -y \
		gcc-m68k-atari-mint \
		mintlib-m68k-atari-mint

WORKDIR /tmp/compile/mintlib-m68k-atari-mint-0.60.1.Git
RUN wget --progress=bar:force:noscroll -O mintlib-0.60.1.Git-20171102.tar.gz \
	https://github.com/freemint/mintlib/archive/ee0ab40a4fdfee26e8f8141076c50f343d9da7be.tar.gz
COPY ${WORKER_NAME}/mintlib/debian debian
RUN dpkg-buildpackage -us -uc
RUN dpkg --install ../mintlib-m68k-atari-mint_0.60.1.Git-*.deb

WORKDIR /tmp/compile/gcc-m68k-atari-mint-7.1.0-mint
RUN wget --progress=bar:force:noscroll -O gcc-7_2_0.tar.gz \
	https://github.com/freemint/m68k-atari-mint-gcc/archive/4984a17029e16071cdf7c0ea0a51ce47c8c11518.tar.gz
COPY ${WORKER_NAME}/gcc/debian debian
RUN dpkg-buildpackage -us -uc
RUN dpkg --install ../gcc-m68k-atari-mint_7.1.0-mint-*.deb

WORKDIR /tmp/compile
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		openssl-m68k-atari-mint \
		sdl-m68k-atari-mint \
		zlib-m68k-atari-mint

RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dpkg-dev \
		pkg-config

COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-freemint.sh ./

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-freemint.sh libpng1.6

COPY common/library-rules/freetype.sh library-rules/
RUN ./compile-libraries-freemint.sh freetype

COPY common/library-rules/libjpeg-turbo.sh library-rules/
RUN ./compile-libraries-freemint.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-freemint.sh faad2

COPY common/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-freemint.sh libmad

RUN ./compile-libraries-freemint.sh libogg

COPY common/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-freemint.sh libtheora

RUN ./compile-libraries-freemint.sh libvorbis

RUN ./compile-libraries-freemint.sh curl

FROM ${DEFAULT_BASE_IMAGE}
USER root
WORKDIR /tmp
COPY --from=compiler \
	/tmp/compile/gcc-m68k-atari-mint_7.1.0-mint-20171102+nmu1_amd64.deb \
	/tmp/compile/mintlib-m68k-atari-mint_0.60.1.Git-20171102+nmu1_amd64.deb \
	/tmp/
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dirmngr \
		gnupg \
		&& \
	apt-key adv \
		--keyserver hkp://keyserver.ubuntu.com:80 \
		--recv-keys BFD8768B6878C33FDFD082C94AAD3A5DB5690522 && \
	echo 'deb http://ppa.launchpad.net/vriviere/ppa/ubuntu zesty main' \
		> /etc/apt/sources.list.d/freemint.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		binutils-m68k-atari-mint \
		libm-m68k-atari-mint \
		libmpc3 \
		libmpfr4 \
		&& \
	dpkg --install mintlib-m68k-atari-mint_0.60.1.Git-20171102+nmu1_amd64.deb && \
	dpkg --install gcc-m68k-atari-mint_7.1.0-mint-20171102+nmu1_amd64.deb && \
	rm *.deb && \
	DEBIAN_FRONTEND=noninteractive apt-get remove -y dirmngr gnupg && \
	DEBIAN_FRONTEND=noninteractive apt-get -y autoremove && \
	DEBIAN_FRONTEND=noninteractive apt-get -y clean && \
	rm -f /etc/apt/sources.list.d/freemint.list && \
	rm -rf /var/lib/apt/lists/*

COPY --from=compiler /usr/m68k-atari-mint /usr/m68k-atari-mint

ENV PATH=$PATH:/usr/m68k-atari-mint/bin \
	ADDR2LINE=m68k-atari-mint-addr2line \
	AR=m68k-atari-mint-ar \
	AS=m68k-atari-mint-as \
	CXX=m68k-atari-mint-c++ \
	CXXFILT=m68k-atari-mint-c++filt \
	CPP=m68k-atari-mint-cpp \
	GXX=m68k-atari-mint-g++ \
	GCC=m68k-atari-mint-gcc \
	GCOV=m68k-atari-mint-gcov \
	GPROF=m68k-atari-mint-gprof \
	LD=m68k-atari-mint-ld \
	NM=m68k-atari-mint-nm \
	OBJCOPY=m68k-atari-mint-objcopy \
	OBJDUMP=m68k-atari-mint-objdump \
	RANLIB=m68k-atari-mint-ranlib \
	SIZE=m68k-atari-mint-size \
	STRINGS=m68k-atari-mint-strings \
	STRIP=m68k-atari-mint-strip

USER buildbot
WORKDIR /buildbot
