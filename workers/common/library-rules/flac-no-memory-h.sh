do_fetch
do_configure

# Some platforms have no memory.h, so libFLAC fails to compile. In those cases,
# what libFLAC really seems to want is string.h.
sed -i -e 's@#include <memory\.h>@#include <string.h>@' src/libFLAC/cpu.c

do_make -C src/libFLAC
do_make -C include
