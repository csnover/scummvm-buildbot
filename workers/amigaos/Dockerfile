ARG DEFAULT_32_BIT_BASE_IMAGE
FROM ${DEFAULT_32_BIT_BASE_IMAGE} AS compiler
ARG WORKER_NAME
USER root

ARG URL=https://github.com/perweij/amigaos-cross-toolchain/archive/014a8b15cb82c77aa138094f638246598858e620.tar.gz

WORKDIR /tmp/compile
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		bison \
		ca-certificates \
		flex \
		g++ \
		gcc \
		make \
		patch \
		python2.7 \
		python2.7-dev \
		python-setuptools \
		subversion \
		wget && \
	rm -rf /var/lib/apt/lists/* && \
	wget --progress=bar:force:noscroll -O - ${URL} |tar xzf -
COPY ${WORKER_NAME}/toolchain-ppc.patch ./
RUN cd amigaos-cross-toolchain*/ && \
	patch -p1 < ../toolchain-ppc.patch && \
	./toolchain-ppc --binutils 2.23.2 --gcc 4.9.1 --prefix /opt/amigaos fetch-all
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		file \
		libncurses-dev && \
	rm -rf /var/lib/apt/lists/*
COPY ${WORKER_NAME}/gcc.patch ./
RUN cd amigaos-cross-toolchain*/ && \
	patch -p1 -d .build-ppc/archives/gcc-4.9.1/ < ../gcc.patch && \
	./toolchain-ppc --binutils 2.23.2 --gcc 4.9.1 --prefix /opt/amigaos build

# dpkg-dev is required to retrieve sources from apt
RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dpkg-dev

RUN sed -i 's/#define SIZE_MAX ULONG_MAX/#define SIZE_MAX 4294967295UL/' /opt/amigaos/ppc-amigaos/SDK/newlib/include/stdint.h

COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-amigaos.sh ./

# Library rules are copied separately along with their corresponding library
# so that changes or additions to individual library scripts don't invalidate
# every single library layer
COPY common/library-rules/zlib.sh library-rules/
RUN ./compile-libraries-amigaos.sh zlib

COPY common/library-rules/bzip2.sh library-rules/
RUN ./compile-libraries-amigaos.sh bzip2

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-amigaos.sh libpng1.6

COPY common/library-rules/freetype.sh library-rules/
RUN ./compile-libraries-amigaos.sh freetype

COPY common/library-rules/libjpeg-turbo.sh library-rules/
RUN ./compile-libraries-amigaos.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-amigaos.sh faad2

COPY common/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-amigaos.sh libmad

RUN ./compile-libraries-amigaos.sh libogg

COPY common/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-amigaos.sh libtheora

RUN ./compile-libraries-amigaos.sh libvorbis

COPY common/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-amigaos.sh mpeg2dec

ARG SDL_URL=https://sourceforge.net/projects/sdl2-amigaos4/files/SDL2_SDK_r177.lha/download
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		lhasa \
		wget && \
	wget --progress=bar:force:noscroll -O sdl.lha ${SDL_URL} && \
	lha x sdl.lha && \
	find SDL2_developer_release -type d -exec chmod 755 {} + && \
	find SDL2_developer_release -type f -exec chmod 644 {} + && \
	cp -RT SDL2_developer_release/SDK/local/newlib/ /opt/amigaos && \
	rm -r SDL2_developer_release sdl.lha && \
	sed -i 's#/SDK/local/newlib/#/opt/amigaos/#g' /opt/amigaos/bin/sdl2-config && \
	chmod 755 /opt/amigaos/bin/sdl2-config

FROM ${DEFAULT_32_BIT_BASE_IMAGE}
USER root
COPY --from=compiler /opt/amigaos /opt/amigaos
ENV PATH=/opt/amigaos/bin:$PATH
USER buildbot
WORKDIR /buildbot
