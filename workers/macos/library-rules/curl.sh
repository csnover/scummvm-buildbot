do_fetch
do_configure --with-darwinssl
do_make -C lib
do_make -C include
make install-pkgconfigDATA
