do_fetch
do_configure --enable-stl --without-libtiff
make -j$num_cpus install
