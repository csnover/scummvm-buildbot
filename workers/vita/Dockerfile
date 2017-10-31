ARG DEFAULT_OS_IMAGE
ARG DEFAULT_BASE_IMAGE
FROM ${DEFAULT_OS_IMAGE} AS compiler
USER root
ARG WORKER_NAME

# dpkg-dev is required to retrieve sources from apt
RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		bzip2 \
		ca-certificates \
		dpkg-dev \
		wget \
		xz-utils

ENV VITASDK=/opt/vitasdk
ENV PATH=$PATH:$VITASDK/bin

ARG URL=https://github.com/vitasdk/autobuilds/releases/download/master-linux-v567/vitasdk-x86_64-linux-gnu-2017-10-29_09-48-44.tar.bz2

RUN wget --progress=bar:force:noscroll -O - $URL \
	| tar --no-same-owner --no-same-permissions -C /opt/ -xjf -

# These insecure, unversioned downloads are not great, but OpenSSL and SDL2 are
# not trivially buildable for this target so we use these packages for the
# moment. At the time of the first build these corresponded to
# https://github.com/vitasdk/packages/commit/b62cb68c349f8f389a4b4e57356c398c43f5531d
# in case someone needs to rebuild them from source later
RUN wget --progress=bar:force:noscroll -O - http://dl.vitasdk.org/openssl.tar.xz \
	| tar --no-same-owner --no-same-permissions -C $VITASDK/arm-vita-eabi -xJf -
RUN wget --progress=bar:force:noscroll -O - http://dl.vitasdk.org/curl.tar.xz \
	| tar --no-same-owner --no-same-permissions -C $VITASDK/arm-vita-eabi -xJf -
RUN wget --progress=bar:force:noscroll -O - http://dl.vitasdk.org/sdl2.tar.xz \
	| tar --no-same-owner --no-same-permissions -C $VITASDK/arm-vita-eabi -xJf -
RUN wget --progress=bar:force:noscroll -O - http://dl.vitasdk.org/sdl_net.tar.xz \
	| tar --no-same-owner --no-same-permissions -C $VITASDK/arm-vita-eabi -xJf -

WORKDIR /tmp/compile
COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-vita.sh ./

COPY common/library-rules/zlib.sh library-rules/
RUN ./compile-libraries-vita.sh zlib

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-vita.sh libpng1.6

COPY common/library-rules/freetype.sh library-rules/
RUN ./compile-libraries-vita.sh freetype

COPY common/library-rules/libjpeg-turbo.sh library-rules/
RUN ./compile-libraries-vita.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-vita.sh faad2

COPY common/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-vita.sh libmad

RUN ./compile-libraries-vita.sh libogg

COPY common/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-vita.sh libtheora

RUN ./compile-libraries-vita.sh libvorbis

COPY common/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-vita.sh mpeg2dec

ENV CFLAGS="$CFLAGS -isystem $VITASDK/include" \
	CXXFLAGS="$CXXFLAGS -isystem $VITASDK/include" \
	LDFLAGS="$LDFLAGS -L $VITASDK/lib"

RUN wget --progress=bar:force:noscroll -O - \
		https://github.com/frangarcj/vita2dlib/archive/fbo.tar.gz \
		| tar -zxf - && \
		cd vita2dlib*/libvita2d && \
		make && \
		mv libvita2d.a $VITASDK/arm-vita-eabi/lib/libvita2d_fbo.a && \
		mv include/vita2d.h $VITASDK/arm-vita-eabi/include/vita2d_fbo.h

RUN wget --progress=bar:force:noscroll -O - \
		https://github.com/frangarcj/vita-shader-collection/releases/download/gtu-0.1-v74/vita-shader-collection.tar.gz \
		| tar --no-same-owner --no-same-permissions -C $VITASDK/arm-vita-eabi -zxf - && \
	mv $VITASDK/arm-vita-eabi/includes/* $VITASDK/arm-vita-eabi/include/ && \
	rmdir $VITASDK/arm-vita-eabi/includes

FROM ${DEFAULT_BASE_IMAGE}
USER root
COPY --from=compiler /opt/vitasdk /opt/vitasdk
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		zip \
		&& \
	rm -rf /var/lib/apt/lists/*

ENV VITASDK=/opt/vitasdk
ENV PATH=$PATH:$VITASDK/bin:$VITASDK/arm-vita-eabi/bin

USER buildbot
WORKDIR /buildbot
