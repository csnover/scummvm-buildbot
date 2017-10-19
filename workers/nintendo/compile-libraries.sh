#!/usr/bin/env bash

toolchains=(
	arm-none-eabi /opt/devkitpro/devkitARM
	powerpc-eabi /opt/devkitpro/devkitPPC
)

orig_path=$PATH
set_toolchain () {
	local target=$1
	local prefix=$2
	local bin_dir="$prefix/bin"

	for bin in addr2line ar as cc c++ gcc cpp c++filt elfedit g++ gcov gdb gprof \
		ld ldd nm objcopy objdump populate ranlib readelf run size strings strip; do
		local var_name=${bin^^}
		var_name=${var_name//+/X}
		local bin_path="$bin_dir/$target-$bin"
		[ -f "$bin_path" ] && export $var_name=$bin_path || unset $var_name
	done

	[ "$CC"  == "" -a "$GCC" != "" ] && export CC=$GCC
	[ "$CXX" == "" -a "$GXX" != "" ] && export CXX=$GXX

	export ACLOCAL_PATH=$prefix/share/aclocal
	export CPPFLAGS="-I$prefix/include"
	export LDFLAGS="-L$prefix/lib"
	export PATH=$bin_dir:$orig_path
	export PKG_CONFIG_LIBDIR=$prefix/lib
	export PKG_CONFIG_PATH=$prefix/lib/pkgconfig
	export PKG_CONFIG_SYSROOT_DIR=$prefix

	if [ "$target" == "arm-none-eabi" ]; then
		export CPPFLAGS="-march=armv6k -mtune=mpcore -mfloat-abi=hard $CPPFLAGS"
		export LDFLAGS="-march=armv6k -mtune=mpcore -mfloat-abi=hard $LDFLAGS"
	fi
}

do_fetch () {
	if [ -d $library*/ ]; then
		rm -r $library*/
	fi
	DEBIAN_FRONTEND=noninteractive apt-get source -y $library
	cd $library*/
}

do_configure () {
	./configure --prefix=$prefix --host=$target --disable-shared $@
}

do_make () {
	make -j$num_cpus install
}

num_cpus=$(grep -c ^processor /proc/cpuinfo)
build_library () {
	target=$1
	prefix=$2
	library=$3

	local rules_file="$root_dir/library-rules/$library.sh"
	if [ -f "$rules_file" ]; then
		. "$rules_file"
	else
		do_fetch
		do_configure
		do_make
	fi

	return 0
}

warning () {
	echo $@ >&2
}

fatal_error () {
	if [ "$library" != "" ]; then
		warning "$library build failed!"
	else
		warning "Build failed!"
	fi
	exit 1
}

set -eE
trap fatal_error ERR

libraries=$@

root_dir=$(pwd)
i=0
while [ $i -lt ${#toolchains[@]} ]; do
	target=${toolchains[i]}
	prefix=${toolchains[$((i+1))]}
	set_toolchain $target $prefix
	env
	for library in $libraries; do
		echo "Building $library"
		build_library $target $prefix $library
		cd "$root_dir"
	done

	i=$((i+2))
done
