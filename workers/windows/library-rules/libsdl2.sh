do_fetch
# Enabling shared libraries for SDL only since it frequently needs to be
# replaced with less buggy earlier/later versions
./configure --prefix=$prefix --host=$host
do_make
$STRIP /usr/$host/bin/SDL2.dll
# If --disable-static is passed, compilation will fail because libSDL2main.a
# won't be built, so just delete the static library so the linker always uses
# the dynamic library even when static linkage is preferred
rm /usr/$host/lib/libSDL2.a
