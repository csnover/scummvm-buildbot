do_fetch
patch -p1 < ../curl-ios.patch
do_configure --with-darwinssl
do_make -C lib
do_make -C include
make install-pkgconfigDATA install-binSCRIPTS
