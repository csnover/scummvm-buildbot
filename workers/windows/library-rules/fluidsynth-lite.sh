get_dependencies ca-certificates cmake wget
wget -O - --progress=bar:force:noscroll \
	https://github.com/dotfloat/fluidsynth-lite/archive/cdc8115d4f2d6e8280759bbe514ba15fa88053ea.tar.gz | tar -xzf -
cd fluidsynth-lite*/
cmake -DCMAKE_INSTALL_PREFIX=$prefix \
	-DCMAKE_SYSTEM_NAME=Windows \
	-DBUILD_SHARED_LIBS=no .
do_make
cp -a src/libfluidsynth.a $prefix/lib
