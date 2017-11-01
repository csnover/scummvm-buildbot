get_dependencies automake libtool
do_fetch

# mpeg2dec assumes that an ARM host will have support pld [r1], but this is not
# the case for armef, so disable the ARM assembly on this platform
sed -i 's/arm\*)/xxarmxx)/' configure

do_configure

# libvo is not needed, and fails to cross-compile for at least Windows, so just
# don't bother to compile it
echo "all install clean:" > libvo/Makefile

# We only want the library, and the utilities fail to compile due to duplicate
# standard library function definitions
echo "all install clean:" > src/Makefile

do_make
