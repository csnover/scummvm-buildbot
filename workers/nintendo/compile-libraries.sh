#!/usr/bin/env bash

toolchains=(arm-none-eabi /opt/devkitpro/devkitARM \
			powerpc-eabi /opt/devkitpro/devkitPPC)

# in alphabetical order, except where dependencies must be ordered
libraries=(
	zlib      # used by libpng
	faad2
	libpng1.6 # used by freetype
	freetype
	libmad
	libogg    # used by libtheora, libvorbis
	libjpeg-turbo
	libtheora
	libvorbis
	mpeg2dec
	# PROBLEMS:
	# curl    - ARM: configure fails, gethostbyname missing
	# flac    - ARM: build fails, utime/chown missing
	# glib2.0 - ARM: configure fails, iconv missing
	# fluidsynth
	# libsdl2
	# libsdl2-net
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

	export CPPFLAGS="-I$prefix/include"
	export LDFLAGS="-L$prefix/lib"
	export PATH=$bin_dir:$orig_path
}

num_cpus=$(grep -c ^processor /proc/cpuinfo)
build_library () {
	local target=$1
	local prefix=$2
	local library=$3

	configure_args="--prefix=$prefix --host=$target --enable-static --disable-shared"
	case $library in
		faad2)
			autoreconf -i || return 1
			;;
		freetype)
			tar xf freetype-2*.tar.bz2
			cd freetype*/
			make || return 1 # this generates `configure`
			;;
		libmad)
			# The libmad package seems a little messed up. For some reason it
			# does not auto-apply quilt patches from the debian directory which
			# are needed to avoid compilation failures due to the use of a flag
			# -fforce-mem which was removed in GCC 4.3.
			dh_quilt_patch || return 1
			touch NEWS AUTHORS ChangeLog
			autoreconf -i || return 1
			;;
		libjpeg-turbo)
			configure_args+="--without-simd"
			;;
		libtheora)
			# Theora tries to build some XML docs even when it can't, and this
			# breaks the build, so just disable that by overwriting the doc
			# Makefile
			echo "all:" > doc/Makefile.am
			echo "all:" > doc/Makefile.in

			configure_args+="--disable-spec --disable-examples"
			;;
		zlib)
			configure_args="--prefix=$prefix --static"
			;;
	esac

	./configure $configure_args || return 1

	make -j$num_cpus && make install || return 1
	return 0
}

warning () {
	echo $@ >&2
}

echo "Building ${libraries[@]}..."

if [ $(grep -c deb-src /etc/apt/sources.list) -eq 0 ]; then
	sed 's/^deb \(.*\)/deb-src \1/' /etc/apt/sources.list > /etc/apt/sources.list.d/sources.list
fi

dev_packages=(
	dpkg-dev
	libgmp10   # required by the ARM compiler
	debhelper  # required by libmad
	quilt      # required by libmad
	pkg-config # required by fluidsynth
)

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ${dev_packages[@]}
DEBIAN_FRONTEND=noninteractive apt-get source -y ${libraries[@]}

root_dir=$(pwd)
i=0
while [ $i -lt ${#toolchains[@]} ]; do
	target=${toolchains[i]}
	prefix=${toolchains[$((i+1))]}
	set_toolchain $target $prefix
	env
	for library in ${libraries[@]}; do
		echo "Building $library"
		cd $library*/
		build_library $target $prefix $library
		if [ $? -ne 0 ]; then
			warning "$library build failed!"
		fi
		cd "$root_dir"
	done

	i=$((i+2))
done
