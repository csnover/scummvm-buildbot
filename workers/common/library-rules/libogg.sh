do_fetch
do_configure
do_make -C src
do_make -C include
make install-m4dataDATA \
	install-pkgconfigDATA
