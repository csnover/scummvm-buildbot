do_fetch
do_configure --without-turbojpeg --without-simd
# libjpeg unconditionally compiles an MD5 hashing utility for
# validation testing, but this tool will not link on the PPC
# compiler, so just get rid of it.
echo "all install clean:" > md5/Makefile
do_make
