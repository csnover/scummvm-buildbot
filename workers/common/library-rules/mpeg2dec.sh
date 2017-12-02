get_dependencies automake libtool
do_fetch

# mpeg2dec assumes that a powerpc host will have altivec, but this is not
# the case for Amiga nor Nintendo PowerPC CPUs, so just disable it always
sed -i 's/have_altivec=yes/have_altivec=no/' configure

do_configure
do_make -C libmpeg2
do_make -C include
