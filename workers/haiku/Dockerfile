ARG DEFAULT_BASE_IMAGE
FROM haiku/cross-compiler:x86-hybrid AS compiler

ARG HPKG_SOURCE=https://packages.haiku-os.org/haikuports/master/hpkg

RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/zlib-1.2.11-2-x86_gcc2.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/zlib_devel-1.2.11-2-x86_gcc2.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/bzip2-1.0.6-5-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/bzip2_devel-1.0.6-5-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libpng16-1.6.29-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libpng16_devel-1.6.29-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/freetype-2.7.1-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/freetype_devel-2.7.1-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/jpeg-9b-4-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/jpeg_devel-9b-4-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/faad2-2.7-2-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/faad2_devel-2.7-2-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libmad-0.15.1b-4-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libmad_devel-0.15.1b-4-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libogg-1.3.2-3-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libogg_devel-1.3.2-3-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libtheora-1.1.1-5-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libtheora_devel-1.1.1-5-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libvorbis-1.3.5-3-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libvorbis_devel-1.3.5-3-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libmpeg2-0.5.1-5-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libmpeg2_devel-0.5.1-5-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libsdl2-2.0.5-3-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/libsdl2_devel-2.0.5-3-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/openssl-1.0.2k-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/openssl_devel-1.0.2k-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/curl-7.53.1-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/curl_devel-7.53.1-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/sdl2_net-2.0.1-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/sdl2_net_devel-2.0.1-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/flac-1.3.1-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg
RUN wget --progress=bar:force:noscroll -O pkg.hpkg \
		${HPKG_SOURCE}/flac_devel-1.3.1-1-x86.hpkg && \
	package extract -C /system pkg.hpkg && \
	rm pkg.hpkg

RUN sed -i 's#/packages/libsdl2-2.0.5-3/.self#/system#g' /system/bin/sdl2-config
RUN sed -e 's#/packages/freetype-2.7.1-1/.self#/system#g' \
		-e 's#/packages/libpng16-1.6.29-1/.self/lib#/system/develop/lib#g' \
		-i /system/bin/freetype-config && \
# ScummVM calls freetype-config with a prefix which causes it to return include
# paths that are invalid for the custom filesystem structure that Haiku uses,
# so just ignore any prefix-setting argument to always get the right value
	perl -0777 -pe 's#prefix=\$optarg\n\s+local_prefix=yes\n##' -i /system/bin/freetype-config

FROM ${DEFAULT_BASE_IMAGE}
USER root
COPY --from=compiler /tools/cross-tools-x86 /tools/cross-tools-x86
COPY --from=compiler /bin/package /usr/local/bin/package
COPY --from=compiler /system /system
COPY --from=compiler \
	/lib/x86_64-linux-gnu/libbe_build.so \
	/lib/x86_64-linux-gnu/libroot_build.so \
	/lib/x86_64-linux-gnu/libpackage_build.so \
	/lib/x86_64-linux-gnu/
COPY --from=compiler /usr/local/bin/jam /usr/local/bin/jam

ENV PATH=/tools/cross-tools-x86/bin:/system/bin:$PATH \
# The compiler will try to link to libstdc++.a and fail due to ABI
# incompatibility because only /system/develop/lib is in the default list of
# search paths
	LDFLAGS="-L /system/lib" \
	ADDR2LINE=i586-pc-haiku-addr2line \
	AR=i586-pc-haiku-ar \
	AS=i586-pc-haiku-as \
	CXX=i586-pc-haiku-c++ \
	CXXFILT=i586-pc-haiku-c++filt \
	CPP=i586-pc-haiku-cpp \
	DLLTOOL=i586-pc-haiku-dlltool \
	DLLWRAP=i586-pc-haiku-dllwrap \
	ELFEDIT=i586-pc-haiku-elfedit \
	GXX=i586-pc-haiku-g++ \
	GCC=i586-pc-haiku-gcc \
	GCOV=i586-pc-haiku-gcov \
	GCOV_TOOL=i586-pc-haiku-gcov-tool \
	GPROF=i586-pc-haiku-gprof \
	LD=i586-pc-haiku-ld \
	NM=i586-pc-haiku-nm \
	OBJCOPY=i586-pc-haiku-objcopy \
	OBJDUMP=i586-pc-haiku-objdump \
	RANLIB=i586-pc-haiku-ranlib \
	READELF=i586-pc-haiku-readelf \
	SIZE=i586-pc-haiku-size \
	STRINGS=i586-pc-haiku-strings \
	STRIP=i586-pc-haiku-strip \
	WINDMC=i586-pc-haiku-windmc \
	WINDRES=i586-pc-haiku-windres

USER buildbot
WORKDIR /buildbot
