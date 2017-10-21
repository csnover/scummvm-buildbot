do_fetch
# mpeg2dec assumes that a powerpc host will have altivec, but this is not the
# case for the Nintendo CPU
sed -i 's/have_altivec=yes/have_altivec=no/' configure
do_configure
do_make
