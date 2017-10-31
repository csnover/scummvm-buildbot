ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE} AS compiler
USER root

WORKDIR /tmp/compile
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dirmngr \
		gnupg && \
	sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-key adv \
		--keyserver hkp://keyserver.ubuntu.com:80 \
		--recv-keys 379CE192D401AB61 && \
	echo 'deb http://dl.bintray.com/sba1/adtools-deb /' \
		> /etc/apt/sources.list.d/adtools.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		adtools-binutils \
		adtools-sdk \
		adtools-gcc \
		dpkg-dev \
# All of this is temporarily necessary because adtools-sdk does not extract the
# pthreads library as of https://github.com/sba1/adtools commit 7ef1f49
		lhasa && \
	wget --progress=bar:force:noscroll -O sdk.lha \
		"http://hyperion-entertainment.biz/index.php/downloads?view=download&format=raw&file=69" && \
	lhasa x sdk.lha SDK_Install/pthread.lha && \
	lhasa x SDK_Install/pthread.lha && \
	find Local/ -type f -exec chmod 644 {} + && \
	cp -Rv Local/* /usr/ppc-amigaos/SDK/ && \
	rm -r sdk.lha SDK_Install/ Local/

ARG WORKER_NAME
COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-amigaos.sh ./

# Library rules are copied separately along with their corresponding library
# so that changes or additions to individual library scripts don't invalidate
# every single library layer
COPY common/library-rules/zlib.sh library-rules/
RUN ./compile-libraries-amigaos.sh zlib

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-amigaos.sh libpng1.6

COPY common/library-rules/freetype.sh library-rules/
RUN ./compile-libraries-amigaos.sh freetype

RUN sed -i 's/#define SIZE_MAX ULONG_MAX/#define SIZE_MAX 4294967295UL/' \
	/usr/ppc-amigaos/SDK/newlib/include/stdint.h
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
	cp -RT SDL2_developer_release/SDK/local/newlib/ /usr/ppc-amigaos && \
	rm -r SDL2_developer_release sdl.lha && \
	sed -i 's#/SDK/local/newlib/#/usr/ppc-amigaos/#g' /usr/ppc-amigaos/bin/sdl2-config && \
	chmod 755 /usr/ppc-amigaos/bin/sdl2-config

# The amigaosdist build target calls this Amiga-only `rx` function; on the old
# buildbot it was just this script that does nothing, on an actual Amiga it
# looks like it is a formatted README generator
RUN printf "#!/bin/sh\ntouch README.guide\n" > /usr/ppc-amigaos/bin/rx && \
	chmod 755 /usr/ppc-amigaos/bin/rx

FROM ${DEFAULT_BASE_IMAGE}
USER root
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dirmngr \
		gnupg && \
	apt-key adv \
		--keyserver hkp://keyserver.ubuntu.com:80 \
		--recv-keys 379CE192D401AB61 && \
	echo 'deb http://dl.bintray.com/sba1/adtools-deb /' \
		> /etc/apt/sources.list.d/adtools.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		adtools-binutils \
		adtools-gcc && \
	apt-get remove -y gnupg dirmngr && \
	apt-get autoremove -y && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY --from=compiler /usr/ppc-amigaos /usr/ppc-amigaos
ENV PATH=$PATH:/usr/ppc-amigaos/bin
USER buildbot
WORKDIR /buildbot
