do_fetch
do_configure --with-ssl=$prefix
do_make -C lib
do_make -C include
make install-pkgconfigDATA
