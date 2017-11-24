do_fetch
# Enabling shared libraries for SDL only since it frequently needs to be
# replaced with less buggy earlier/later versions
./configure --prefix=$prefix --host=$host
# We do not want to have to include libgcc DLL at runtime, so we need
# -static-libgcc, but libtool strips things from $LDFLAGS because SDL2
# is a library build, so we have to pass it using this special -Wc syntax to
# keep libtool from stripping it
make -j$num_cpus LDFLAGS="$LDFLAGS -Wc,-static-libgcc" install
$STRIP /usr/$host/bin/SDL2.dll
# If --disable-static is passed, compilation will fail because libSDL2main.a
# won't be built, so just delete the static library so the linker always uses
# the dynamic library even when static linkage is preferred
rm /usr/$host/lib/libSDL2.a
