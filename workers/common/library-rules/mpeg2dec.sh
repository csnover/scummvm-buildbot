get_dependencies automake libtool
do_fetch

# mpeg2dec assumes that a powerpc host will have altivec, but this is not
# the case for Amiga nor Nintendo PowerPC CPUs, so just disable it always
sed -i 's/have_altivec=yes/have_altivec=no/' configure

do_configure

# libvo is not needed, and fails to cross-compile for at least Windows, so just
# don't bother to compile it
echo "all install clean:" > libvo/Makefile

# We only want the library, and the utilities fail to compile due to duplicate
# standard library function definitions
echo "all install clean:" > src/Makefile

do_make
