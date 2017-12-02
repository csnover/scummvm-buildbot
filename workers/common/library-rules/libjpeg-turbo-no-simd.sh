do_fetch
do_configure --without-turbojpeg --without-simd
make -j$num_cpus \
	install-libLTLIBRARIES \
	install-pkgconfigDATA \
	install-includeHEADERS \
	install-nodist_includeHEADERS
