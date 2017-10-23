FROM debian:stretch-slim AS builder

RUN apt-get update && \
	apt-get install -y \
		autoconf \
		automake \
		bison \
		bzip2 \
		flex \
		g++ \
		gcc \
		git \
		libelf-dev \
		libgmp3-dev \
		libncurses5-dev \
		libssl-dev \
		libtool-bin \
		make \
		mercurial \
		patch \
		pkg-config \
		python \
		python-dev \
		texinfo \
		wget \
		zlib1g-dev

ENV PS3DEV  /ps3dev
ENV PSL1GHT $PS3DEV
ENV PATH    $PATH:$PS3DEV/bin:$PS3DEV/ppu/bin:$PS3DEV/spu/bin

# For now the `for-scummvm` branch of the `bgK` fork of `ps3toolchain` is used to get GCC 7.2.0.
# Ideally those changes are merged upstream, and the main `ps3dev/ps3toolchain` repository can be used.
RUN wget --no-check-certificate https://github.com/bgK/ps3toolchain/tarball/for-scummvm -O ps3toolchain.tar.gz \
		&& mkdir /ps3toolchain && tar --strip-components=1 --directory=/ps3toolchain -xvzf ps3toolchain.tar.gz

WORKDIR /ps3toolchain
RUN ./toolchain.sh

RUN hg clone https://bitbucket.org/bgK/sdl_psl1ght/ /sdl -r psl1ght-2.0.3
WORKDIR /sdl
RUN ./script.sh && make && make install 

FROM ${DEFAULT_BASE_IMAGE}
USER root
ARG WORKER_NAME

ENV PS3DEV  /ps3dev
ENV PSL1GHT $PS3DEV
ENV PATH    $PATH:$PS3DEV/bin:$PS3DEV/ppu/bin:$PS3DEV/spu/bin

COPY --from=builder /ps3dev /ps3dev

RUN apt-get update && \
	apt-get install -y \
		libelf1 \
		libgmp10 \
		libssl1.1 \
		python \
		&& \
	rm -rf /var/lib/apt/lists/*

USER buildbot
WORKDIR /buildbot

