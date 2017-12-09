ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE} AS builder
USER root

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

RUN wget https://github.com/ps3dev/ps3toolchain/archive/71e9c0222ca4f0d3041a45b6821c05f390b27fa3.tar.gz -O ps3toolchain.tar.gz \
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
