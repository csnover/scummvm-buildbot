get_dependencies gcc libc6-dev
do_fetch
tar xf freetype-2*.tar.bz2
cd freetype*/
do_configure
do_make
