# Using the 64-bit Debian image here just to reduce the number of layers with
# redundant data in them; DEFAULT_BASE_IMAGE would work fine too
FROM scummvm/buildbot-debian-x86_64:latest AS compiler
USER root
ARG WORKER_NAME

WORKDIR /tmp/compile
# dpkg-dev is required to retrieve sources from apt
RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dpkg-dev \
		libz-mingw-w64-dev \
		mingw-w64

WORKDIR /tmp/compile
# There are two problems with the sysroots that Debian sets up for the mingw-w64
# cross-compiler:
# (1) Unprefixed links are set up to a selection of cross-compiler binaries,
#     which breaks compilation of things like FreeType which need access to the
#     host system's compiler and assumes the unprefixed binaries are the native
#     compiler binaries;
# (2) Links aren't set up to the prefixed compilers, so compile-libraries.sh
#     doesn't find them and fails
# To address these, we delete all the binaries and then generate our own links
# here.
RUN for arch in i686 x86_64; do \
		rm /usr/$arch-w64-mingw32/bin/* && \
		for bin in /usr/bin/$arch-w64-mingw32-*; do \
			ln -s $bin /usr/$arch-w64-mingw32/bin/$(basename $bin); \
		done \
	done

COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-windows.sh ./

COPY common/library-rules/bzip2.sh library-rules/
RUN ./compile-libraries-windows.sh bzip2

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-windows.sh libpng1.6

COPY common/library-rules/freetype.sh library-rules/
RUN ./compile-libraries-windows.sh freetype

COPY common/library-rules/libjpeg-turbo.sh library-rules/
RUN ./compile-libraries-windows.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-windows.sh faad2

COPY common/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-windows.sh libmad

RUN ./compile-libraries-windows.sh libogg

COPY common/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-windows.sh libtheora

RUN ./compile-libraries-windows.sh libvorbis

COPY ${WORKER_NAME}/library-rules/curl.sh library-rules/
RUN ./compile-libraries-windows.sh curl
RUN ./compile-libraries-windows.sh libsdl2

COPY ${WORKER_NAME}/library-rules/libsdl2-net.sh library-rules/
RUN ./compile-libraries-windows.sh libsdl2-net

COPY ${WORKER_NAME}/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-windows.sh mpeg2dec

FROM scummvm/buildbot-debian-x86_64:latest
USER root

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		libz-mingw-w64-dev \
		mingw-w64 \
		zip \
		&& \
	rm -rf /var/lib/apt/lists/*

COPY --from=compiler /usr/i686-w64-mingw32 /usr/i686-w64-mingw32
COPY --from=compiler /usr/x86_64-w64-mingw32 /usr/x86_64-w64-mingw32

USER buildbot
WORKDIR /buildbot
