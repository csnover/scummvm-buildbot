do_fetch
# The SDL library/include prefixes will get duplicated if only --prefix is
# provided to configure so we also pass --with-sdl-prefix
# Shared libraries also enabled for SDL only since it frequently needs to be
# replaced with less buggy earlier/later versions
./configure --prefix=$prefix --host=$host --with-sdl-prefix=$prefix --disable-static
do_make
$STRIP /usr/$host/bin/SDL2_net.dll
