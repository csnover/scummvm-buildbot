get_dependencies automake pkg-config
do_fetch
autoreconf -i
do_configure --enable-low-accuracy
make -j$num_cpus \
	install-libLTLIBRARIES \
	install-includeHEADERS \
	install-pkgconfigDATA
