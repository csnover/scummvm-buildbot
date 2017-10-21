get_dependencies automake pkg-config
do_fetch
autoreconf -i
do_configure --enable-low-accuracy
do_make
