do_fetch
./config no-shared --prefix=$prefix
make -j$num_cpus build_libs
make install_dev
