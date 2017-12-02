do_fetch
do_configure
make -j$num_cpus \
	install-libLTLIBRARIES \
	install-binSCRIPTS \
	install-pkgconfigDATA \
	install-pkgincludeHEADERS \
	install-nodist_pkgincludeHEADERS
make \
	install-header-links \
	install-library-links \
	install-libpng-pc
