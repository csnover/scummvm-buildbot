do_fetch

# When PIC is enabled, the compiler generates R_ARM_BASE_PREL relocations (and
# probably some R_ARM_GOTOFF32 and R_ARM_GOT_BREL too since it is generating
# .data.rel.ro, .rel.data.rel.ro, and .got sections) but vita-elf-create does
# not know how to handle these so it throws an error and exits when processing
# the (valid!) generated binary. The defective method is get_rel_handling in
# vita-elf.c,
# https://github.com/vitasdk/vita-toolchain/blob/5c78cd5a14d5b3c9c46c93b67cd52e7c312fd7fe/src/vita-elf.c#L184
# For now we disable PIC for this library to get rid of these relocations,
# though this could easily come up again at some point in the future if the
# compiler decides to use a global offset table again, so upstream really ought
# to fix their code before we break in a way that we *can’t* fix with a hack
# like this.
do_configure --without-pic

# Some platforms have no memory.h, so libFLAC fails to compile. In those cases,
# what libFLAC really seems to want is string.h.
sed -i -e 's@#include <memory\.h>@#include <string.h>@' src/libFLAC/cpu.c

do_make -C src/libFLAC
do_make -C include
