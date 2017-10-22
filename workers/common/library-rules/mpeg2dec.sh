get_dependencies automake libtool
do_fetch

if [ "$host" == "powerpc-eabi" ]; then
	# mpeg2dec assumes that a powerpc host will have altivec, but this is not the
	# case for the Nintendo CPU
	sed -i 's/have_altivec=yes/have_altivec=no/' configure
fi

do_configure

if [[ $host == arm-apple-darwin* ]]; then
	# the ARM assembler for iOS cannot process .internal directives, so undo the
	# patch that adds them or compilation will fail
	patch -R -p1 < debian/patches/60_arm-private-symbols.patch

	# Fix missing leading underscores in .global symbols in arm asm
	sed -i 's/MC_put_o_16_arm/_MC_put_o_16_arm/' libmpeg2/motion_comp_arm_s.S
	sed -i 's/MC_put_o_8_arm/_MC_put_o_8_arm/' libmpeg2/motion_comp_arm_s.S
	sed -i 's/MC_put_x_16_arm/_MC_put_x_16_arm/' libmpeg2/motion_comp_arm_s.S
	sed -i 's/MC_put_x_8_arm/_MC_put_x_8_arm/' libmpeg2/motion_comp_arm_s.S

	# We only want the library, and the utilities fail to compile for an unclear
	# reason
	echo "all install clean:" > src/Makefile
fi

do_make
