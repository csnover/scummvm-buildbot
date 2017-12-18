#!/usr/bin/env bash

usage() {
	echo "Usage: $0 [--help] <host> <prefix> <library> [<library> ...]"
	echo
	echo "Builds libraries for the given cross-compiler toolchain."
	echo
	echo "<host>:    The host tuple (e.g. arm-apple-darwin11)."
	echo "<prefix>:  The absolute path to the cross-compiler's root directory"
	echo "           (i.e. the directory containing bin, lib, etc.)."
	echo "<library>: The name of the library source package."
}

root_dir=$PWD
flags=()
orig_path=$PATH
set_toolchain () {
	local host=$1
	local prefix=$2
	local bin_dir="$prefix/bin"

	for bin in $(find $bin_dir ${PATH//:/ } -maxdepth 1 -name "$host-*"); do
		local bin_name=$(basename $bin)
		bin_name=${bin_name#$host-}
		local var_name=${bin_name^^}
		var_name=${var_name//+/X}
		var_name=$(echo -n $var_name |sed "s/[^A-Z0-9_]/_/g")
		export $var_name=$bin
	done

	# Preferring non-generic compiler binary names in CC/CXX, because on at
	# least Android, clang/clang++ are wrappers which set the correct API level,
	# and cc/c++ are the actual compilers, and not having the correct API level
	# screws up system headers which were changed between API versions

	if [ "$CLANG" != "" ]; then
		export CC=$CLANG
	elif [ "$GCC" != "" ]; then
		export CC=$GCC
	elif [ "$CC" == "" ]; then
		warning "Could not find a C compiler"
		exit 1
	fi

	if [ "$CLANGXX" != "" ]; then
		export CXX=$CLANGXX
	elif [ "$GXX" != "" ]; then
		export CXX=$GXX
	elif [ "$CXX" == "" ]; then
		warning "Could not find a C++ compiler"
		exit 1
	fi

	export ACLOCAL_PATH=$prefix/share/aclocal
	export PKG_CONFIG_LIBDIR=$prefix/lib
	export PKG_CONFIG_PATH=$prefix/lib/pkgconfig
}

get_dependencies () {
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $@
}

do_fetch () {
	if [ -d $library*/ ]; then
		rm -r $library*/
	fi
	DEBIAN_FRONTEND=noninteractive apt-get source -y $library
	cd $library*/
}

do_configure () {
	./configure --prefix=$prefix --host=$host --disable-shared $@
}

do_make () {
	make -j$num_cpus install $@
}

num_cpus=$(nproc || grep -c ^processor /proc/cpuinfo || echo 1)
build_library () {
	host=$1
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
	warning "You may now connect to the container with docker exec to inspect"
	warning "the environment, then hit Ctrl+C here to end the build."
	tail -f /dev/null
	exit 1
}

set -eE
trap fatal_error ERR

while [ $# -gt 0 ]; do
	case arg in
		--help)
			usage
			exit 0
			;;
		*)
			break
			;;
	esac
done

if [ $# -lt 3 ]; then
	usage
	echo
	echo "Error: Missing required arguments."
	exit 1
fi

host=$1
prefix=$2
shift 2
libraries=$@

set_toolchain $host $prefix
env
for library in $libraries; do
	echo "Building $library"
	build_library $host $prefix $library
	cd "$root_dir"
done
