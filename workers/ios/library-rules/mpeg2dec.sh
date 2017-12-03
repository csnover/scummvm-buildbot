get_dependencies automake libtool
do_fetch

do_configure

# the ARM assembler for iOS cannot process .internal directives, so undo the
# patch that adds them or compilation will fail
patch -R -p1 < debian/patches/60_arm-private-symbols.patch

# Fix missing leading underscores in .global symbols in arm asm
sed -i 's/MC_put_o_16_arm/_MC_put_o_16_arm/' libmpeg2/motion_comp_arm_s.S
sed -i 's/MC_put_o_8_arm/_MC_put_o_8_arm/' libmpeg2/motion_comp_arm_s.S
sed -i 's/MC_put_x_16_arm/_MC_put_x_16_arm/' libmpeg2/motion_comp_arm_s.S
sed -i 's/MC_put_x_8_arm/_MC_put_x_8_arm/' libmpeg2/motion_comp_arm_s.S

do_make -C libmpeg2
do_make -C include
