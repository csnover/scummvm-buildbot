ARG DEFAULT_BASE_IMAGE
FROM ticky/pspdev AS pspdev
FROM ${DEFAULT_BASE_IMAGE}
COPY --from=pspdev /pspdev /pspdev
USER root
# In at least Docker 17.09 these ENV commands need to be separate since
# otherwise references to $PSPDEV and $PSPSDK will be missing
ENV PSPDEV /pspdev
ENV PSPSDK $PSPDEV/psp
ENV PATH=$PATH:$PSPDEV/bin:$PSPSDK/bin \
	CXXFLAGS="$CXXFLAGS -isystem /pspdev/psp/sdk/include" \
	LDFLAGS="$LDFLAGS -L /pspdev/psp/sdk/lib" \
	ADDR2LINE=psp-addr2line \
	AR=psp-ar \
	AS=psp-as \
	CXX=psp-c++ \
	CXXFILT=psp-c++filt \
	CMAKE=psp-cmake \
	CPP=psp-cpp \
	ELFEDIT=psp-elfedit \
	GXX=psp-g++ \
	GCC=psp-gcc \
	GCOV=psp-gcov \
	GDB=psp-gdb \
	LD=psp-ld \
	NM=psp-nm \
	OBJCOPY=psp-objcopy \
	OBJDUMP=psp-objdump \
	RANLIB=psp-ranlib \
	READELF=psp-readelf \
	SIZE=psp-size \
	STRINGS=psp-strings \
	STRIP=psp-strip

USER buildbot
WORKDIR /buildbot
