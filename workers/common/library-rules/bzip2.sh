# This library only needs to be compiled if you are planning on using a
# precompiled FreeType that expects it to exist. Otherwise, it is used only for
# an obsolete X11 bitmap font format that ScummVM will never use.

do_fetch

# Manually build and install only the static library and header
make -j$num_cpus PREFIX="$prefix" CC="$CC" LDFLAGS="$LDFLAGS" AR="$AR" RANLIB="$RANLIB" CFLAGS="$CFLAGS" libbz2.a
mkdir -p "$prefix/lib"
cp -f libbz2.a "$prefix/lib"
chmod a+r "$prefix/lib/libbz2.a"
mkdir -p "$prefix/include"
cp -f bzlib.h "$prefix/include"
chmod a+r "$prefix/include/bzlib.h"
