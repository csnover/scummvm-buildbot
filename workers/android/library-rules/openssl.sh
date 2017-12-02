do_fetch
patch -p1 < ../openssl-clang.patch
CROSS_SYSROOT=/opt/android/arm/sysroot ARCH_SYSROOT=$CROSS_SYSROOT \
	./Configure no-shared --prefix=$prefix android-clang
CROSS_SYSROOT=/opt/android/arm/sysroot ARCH_SYSROOT=$CROSS_SYSROOT \
	make -j$num_cpus build_libs
CROSS_SYSROOT=/opt/android/arm/sysroot ARCH_SYSROOT=$CROSS_SYSROOT \
	make install_dev
