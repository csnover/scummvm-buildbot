get_dependencies automake libtool
do_fetch

# mpeg2dec assumes that a powerpc host will have altivec, but this is not
# the case for Amiga nor Nintendo PowerPC CPUs, so just disable it always
sed -i 's/have_altivec=yes/have_altivec=no/' configure

# For some currently unknown reason, inlining functions from stdlib.h fails and
# causes duplicate definitions with mingw-w64, so disable the inlining
export CFLAGS="$CFLAGS -D__CRT__NO_INLINE"

do_configure

# libvo is not needed, and fails to cross-compile for at least 64-bit Windows,
# so just don't bother to compile it
echo "all install clean:" > libvo/Makefile

# We only want the library, and the utilities fail to compile due to duplicate
# standard library function definitions
echo "all install clean:" > src/Makefile

do_make
