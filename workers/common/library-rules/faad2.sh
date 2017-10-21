get_dependencies automake libtool
do_fetch
autoreconf -i
do_configure
do_make
