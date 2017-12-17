ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE} AS compiler
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
		mingw-w64 \
		nasm \
		pkg-config

WORKDIR /tmp/compile
COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-windows.sh ./

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

COPY common/library-rules/libogg.sh library-rules/
RUN ./compile-libraries-windows.sh libogg

COPY common/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-windows.sh libtheora

COPY common/library-rules/libvorbis.sh library-rules/
RUN ./compile-libraries-windows.sh libvorbis

COPY common/library-rules/flac.sh library-rules/
RUN ./compile-libraries-windows.sh flac

COPY ${WORKER_NAME}/library-rules/curl.sh library-rules/
RUN ./compile-libraries-windows.sh curl

COPY ${WORKER_NAME}/library-rules/libsdl2.sh library-rules/
RUN ./compile-libraries-windows.sh libsdl2

COPY ${WORKER_NAME}/library-rules/libsdl2-net.sh library-rules/
RUN ./compile-libraries-windows.sh libsdl2-net

COPY ${WORKER_NAME}/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-windows.sh mpeg2dec

# Expat and wxWidgets are used only for ScummVM Tools
RUN ./compile-libraries-windows.sh expat

COPY ${WORKER_NAME}/library-rules/wxwidgets3.0.sh library-rules/
RUN ./compile-libraries-windows.sh wxwidgets3.0

# All of this is for FluidSynth
RUN apt-get install -y --no-install-recommends cmake

RUN ./compile-libraries-windows.sh libffi

COPY ${WORKER_NAME}/library-rules/gettext.sh library-rules/
RUN ./compile-libraries-windows.sh gettext

COPY ${WORKER_NAME}/library-rules/glib2.0.sh library-rules/
COPY ${WORKER_NAME}/glib2.0-no-dllmain.patch ./
RUN ./compile-libraries-windows.sh glib2.0

COPY ${WORKER_NAME}/library-rules/fluidsynth.sh library-rules/
RUN ./compile-libraries-windows.sh fluidsynth

ARG SPARKLE_VERSION=0.5.7

WORKDIR /tmp
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		unzip \
		wget && \
	wget --progress=bar:force:noscroll -O sparkle.zip \
		https://github.com/vslavik/winsparkle/releases/download/v${SPARKLE_VERSION}/WinSparkle-${SPARKLE_VERSION}.zip && \
	unzip sparkle.zip && \
	cd WinSparkle-${SPARKLE_VERSION} && \
	cp -a include/* /usr/i686-w64-mingw32/include && \
	cp -a include/* /usr/x86_64-w64-mingw32/include && \
	mv Release/* /usr/i686-w64-mingw32/lib && \
	mv x64/Release/* /usr/x86_64-w64-mingw32/lib && \
	cd .. && \
	rm -r WinSparkle-${SPARKLE_VERSION} sparkle.zip

# Using the 64-bit Debian image here just to reduce the number of layers with
# redundant data in them; DEFAULT_BASE_IMAGE would work fine too
FROM scummvm/buildbot-debian-x86_64:latest
USER root

# i386 arch is for wine32
RUN dpkg --add-architecture i386 && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		dos2unix \
		libz-mingw-w64-dev \
		mingw-w64 \
		nasm \
# For ScummVM Tools
		win-iconv-mingw-w64-dev \
# For Inno Setup
		wget \
		wine \
		wine32 \
		xauth \
		xvfb \
		&& \
	rm -rf /var/lib/apt/lists/*

COPY --from=compiler /usr/i686-w64-mingw32 /usr/i686-w64-mingw32
COPY --from=compiler /usr/x86_64-w64-mingw32 /usr/x86_64-w64-mingw32

# Hacky way to force use of static libz
RUN bash -c 'rm /usr/{x86_64,i686}-w64-mingw32/lib/{libz.dll.a,zlib1.dll}'

ARG INNOSETUP_VERSION=5.5.9

# Wine apparently refuses to do anything if the Wine directory is not owned by
# the current user, so we have to switch and do everything from the Buildbot
# user
USER buildbot
# Using the Netherlands URL because the US one is not HTTPS
RUN wget --progress=bar:force:noscroll -O innosetupsetup.exe \
		https://mlaan2.home.xs4all.nl/ispack/innosetup-${INNOSETUP_VERSION}-unicode.exe && \
	if ! HOME=/buildbot xvfb-run wine innosetupsetup.exe /SP- /VERYSILENT /SUPPRESSMSGBOXES /LOG=install.log; then \
		cat install.log ; exit 1 ; \
	fi && \
	rm innosetupsetup.exe install.log && \
	wget --progress=bar:force:noscroll \
		-O "/buildbot/.wine/drive_c/Program Files/Inno Setup 5/Languages/Swedish.isl" \
		https://raw.github.com/jrsoftware/issrc/master/Files/Languages/Unofficial/Swedish.isl

ENV LDFLAGS="$LDFLAGS -static-libgcc"

USER buildbot
WORKDIR /buildbot
