get_dependencies automake libtool
do_fetch

# For some currently unknown reason, inlining functions from stdlib.h fails and
# causes duplicate definitions with mingw-w64, so disable the inlining
export CFLAGS="$CFLAGS -D__CRT__NO_INLINE"

do_configure
do_make -C libmpeg2
do_make -C include
