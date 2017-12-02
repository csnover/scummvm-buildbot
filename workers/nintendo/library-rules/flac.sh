do_fetch

# The GC/Wii PPC does not support AltiVec
do_configure --disable-altivec

do_make -C src/libFLAC
do_make -C include
