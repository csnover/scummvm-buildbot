do_fetch
# The SDL library/include prefixes will get duplicated if only --prefix is
# provided to configure
do_configure --with-sdl-prefix=$prefix
do_make
