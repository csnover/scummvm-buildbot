do_fetch
do_configure --with-winssl
do_make -C lib
do_make -C include
make install-pkgconfigDATA
