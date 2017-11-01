ARG DEFAULT_BASE_IMAGE
ARG DEFAULT_OS_IMAGE
FROM ${DEFAULT_OS_IMAGE} AS compiler
USER root
ARG WORKER_NAME

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		openjdk-8-jre-headless \
		python \
		unzip \
		wget && \
	rm -rf /var/lib/apt/lists/*

ARG NDK_VERSION=r15c
WORKDIR /tmp/compile
RUN mkdir -p /opt/android/arm/ && \
	wget --progress=bar:force:noscroll -O sdk.zip \
		https://dl.google.com/android/repository/android-ndk-${NDK_VERSION}-linux-x86_64.zip && \
	unzip sdk.zip && \
	rm sdk.zip

# 14 is the minimum supported API version by modern NDKs.
ARG PLATFORM_API_VERSION=14
RUN cd android-ndk-*/ && \
	python ./build/tools/make_standalone_toolchain.py \
		--arch arm \
		--install-dir /opt/android/arm \
		--api ${PLATFORM_API_VERSION} \
		--force && \
# All these acrobatics, plus the build tools and sources, are needed for
# ndk-build. They may not all be needed for future builds that use CMake+Gradle
# instead.
	mkdir -p /opt/android/toolchains/arm-linux-androideabi-4.9/prebuilt/ && \
	ln -s /opt/android/arm/ \
		/opt/android/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64 && \
	mv build /opt/android/build && \
	mv sources /opt/android/sources && \
	mkdir -p /opt/android/platforms/android-${PLATFORM_API_VERSION}/ && \
	ln -s /opt/android/arm/sysroot /opt/android/platforms/android-${PLATFORM_API_VERSION}/arch-arm && \
# android-23 is needed separately because the code is compiled for API 14, but
# the packaging is done for API 23, apparently for some vague manifest-related
# reason in commit a32c53f936f8b3fbf90d016d3c07de62c96798b1
	mkdir -p /opt/android/platforms/android-23/ && \
	mv platforms/android-23/arch-arm /opt/android/platforms/android-23/arch-arm && \
	rm -rf /tmp/compile

# TODO: We are forced to use this older version of the SDK tools because ScummVM
# uses the obsolete ndk-build process instead of the newer CMake+Gradle process.
ARG SDK_VERSION=r25.2.5
WORKDIR /tmp/compile
RUN wget --progress=bar:force:noscroll -O sdk.zip \
		https://dl.google.com/android/repository/tools_${SDK_VERSION}-linux.zip && \
	unzip sdk.zip -d /opt/android/sdk && \
	rm sdk.zip && \
# we could probably prune tools files even more aggressively for space, if
# needed
	rm -rf \
		/opt/android/sdk/tools/apps \
		/opt/android/sdk/tools/lib/monitor-x86 \
		/opt/android/sdk/tools/lib/monitor-x86_64 \
		/opt/android/sdk/tools/lib64 \
		/opt/android/sdk/tools/proguard \
		/opt/android/sdk/tools/qemu \
		&& \
	find /opt/android/sdk -type f -executable -exec chmod o+x {} + && \
# android-23 is needed because the code is compiled for API 14, but the
# packaging is done for API 23, apparently for some vague manifest-related
# reason in commit a32c53f936f8b3fbf90d016d3c07de62c96798b1
	yes | /opt/android/sdk/tools/bin/sdkmanager \
		"build-tools;25.0.3" \
		platform-tools \
		"platforms;android-23" && \
# ndk-build is apparently just broken as it calls a non-executable script with
# no shebang
	chmod 755 /opt/android/build/extract_platform.py && \
	sed -i "1s|^|#!$(which python)\n|" /opt/android/build/extract_platform.py

# dpkg-dev is required to retrieve sources from apt
RUN sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list \
		> /etc/apt/sources.list.d/debsrc.list && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		debhelper \
		dpkg-dev \
		libncurses5 \
		pkg-config

ENV PATH=$PATH:/opt/android/arm/bin

WORKDIR /tmp/compile
COPY common/compile-libraries.sh ${WORKER_NAME}/compile-libraries-android.sh ./

# Android comes with a suitable zlib already

COPY common/library-rules/libpng1.6.sh library-rules/
RUN ./compile-libraries-android.sh libpng1.6

COPY common/library-rules/freetype.sh library-rules/
RUN ./compile-libraries-android.sh freetype

COPY common/library-rules/libjpeg-turbo.sh library-rules/
RUN ./compile-libraries-android.sh libjpeg-turbo

COPY common/library-rules/faad2.sh library-rules/
RUN ./compile-libraries-android.sh faad2

COPY ${WORKER_NAME}/library-rules/libmad.sh library-rules/
RUN ./compile-libraries-android.sh libmad

RUN ./compile-libraries-android.sh libogg

COPY ${WORKER_NAME}/library-rules/libtheora.sh library-rules/
RUN ./compile-libraries-android.sh libtheora

RUN ./compile-libraries-android.sh libvorbis

COPY common/library-rules/flac.sh library-rules/
RUN ./compile-libraries-android.sh flac

COPY ${WORKER_NAME}/library-rules/mpeg2dec.sh library-rules/
RUN ./compile-libraries-android.sh mpeg2dec

RUN ./compile-libraries-android.sh libsdl2
RUN ./compile-libraries-android.sh curl

COPY common/library-rules/libsdl2-net.sh library-rules/
RUN ./compile-libraries-android.sh libsdl2-net

FROM ${DEFAULT_BASE_IMAGE}
USER root
COPY --from=compiler /opt/android /opt/android
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
# The compiler needs libncurses5; the SDK build tools need file and Java, the
# ScummVM build needs ant
		ant \
		file \
		libncurses5 \
		openjdk-8-jdk-headless && \
	rm -rf /var/lib/apt/lists/*

ENV PATH=$PATH:/opt/android/arm/bin \
	ADDR2LINE=arm-linux-androideabi-addr2line \
	AR=arm-linux-androideabi-ar \
	AS=arm-linux-androideabi-as \
	CXX=arm-linux-androideabi-c++ \
	CXXFILT=arm-linux-androideabi-c++filt \
	CXXFLAGS="--sysroot=/opt/android/arm/sysroot" \
	LDFLAGS="--sysroot=/opt/android/arm/sysroot -lgnustl_shared" \
	CC=arm-linux-androideabi-clang \
	CPP=arm-linux-androideabi-cpp \
	DWP=arm-linux-androideabi-dwp \
	ELFEDIT=arm-linux-androideabi-elfedit \
	GXX=arm-linux-androideabi-g++ \
	GCC=arm-linux-androideabi-gcc \
	GCOV=arm-linux-androideabi-gcov \
	GCOV_TOOL=arm-linux-androideabi-gcov-tool \
	GPROF=arm-linux-androideabi-gprof \
	LD=arm-linux-androideabi-ld \
	NM=arm-linux-androideabi-nm \
	OBJCOPY=arm-linux-androideabi-objcopy \
	OBJDUMP=arm-linux-androideabi-objdump \
	RANLIB=arm-linux-androideabi-ranlib \
	READELF=arm-linux-androideabi-readelf \
	SIZE=arm-linux-androideabi-size \
	STRINGS=arm-linux-androideabi-strings \
	STRIP=arm-linux-androideabi-strip

USER buildbot
WORKDIR /buildbot
