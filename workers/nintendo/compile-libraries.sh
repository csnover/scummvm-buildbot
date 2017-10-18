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
}

num_cpus=$(grep -c ^processor /proc/cpuinfo)
build_library () {
	local target=$1
	local prefix=$2
	local library=$3

	make clean 2>&1 >/dev/null

	configure="./configure"
	configure_args="--prefix=$prefix --host=$target --enable-static --disable-shared "
	case $library in
		faad2)
			autoreconf -i || return 1
			;;
		flac)
			configure_args+="--disable-altivec"
			;;
		freetype)
			tar xf freetype-2*.tar.bz2 || return 1
			cd freetype*/ || return 1
			;;
		libjpeg-turbo)
			configure_args+="--without-turbojpeg --without-simd"
			;;
		libmad)
			# Unlike the other packages, for some reason libmad does not
			# auto-apply quilt patches from the debian directory, which are
			# needed to (among other things) avoid compilation failures due to
			# the use of a flag `-fforce-mem`` which was removed in GCC 4.3.
			dh_quilt_patch || return 1
			touch NEWS AUTHORS ChangeLog || return 1
			autoreconf -i || return 1
			;;
		libpng1.6)
			# libpng unconditionally compiles some tools which try to link to
			# interfaces that do not exist on GC/Wii. There is no flag to
			# disable these compilations, so just empty out the affected tool
			# for now.
			echo "int main() { return 0; }" > contrib/tools/pngcp.c
			;;
		libtheora)
			# Theora tries to build some XML docs even when it can't, and this
			# breaks the build, so just disable that by overwriting the doc
			# Makefile.
			echo "all install clean:" > doc/Makefile.am
			echo "all install clean:" > doc/Makefile.in

			configure_args+="--disable-spec --disable-examples"
			;;
		libvorbisidec)
			autoreconf -i || return 1
			configure_args+="--enable-low-accuracy"
			;;
		mpeg2dec)
			sed -i 's/have_altivec=yes/have_altivec=no/' configure
			;;
		zlib)
			configure_args="--prefix=$prefix --static"
			;;
	esac

	$configure $configure_args || return 1

	case $library in
		libjpeg-turbo)
			# libjpeg unconditionally compiles an MD5 hashing utility for
			# validation testing, but this tool will not link on the PPC
			# compiler, so just get rid of it.
			echo "all install clean:" > md5/Makefile
		;;
	esac

	make -j$num_cpus install || return 1

	return 0
}

warning () {
	echo $@ >&2
}

libraries=$@

DEBIAN_FRONTEND=noninteractive apt-get source -y $libraries

root_dir=$(pwd)
i=0
while [ $i -lt ${#toolchains[@]} ]; do
	target=${toolchains[i]}
	prefix=${toolchains[$((i+1))]}
	set_toolchain $target $prefix
	env
	for library in $libraries; do
		echo "Building $library"
		cd $library*/
		build_library $target $prefix $library
		if [ $? -ne 0 ]; then
			warning "$library build failed!"
			exit 1
		fi
		cd "$root_dir"
	done

	i=$((i+2))
done
