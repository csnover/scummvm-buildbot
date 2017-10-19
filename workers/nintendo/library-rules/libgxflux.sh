if [ $target == "powerpc-eabi" ]; then
	wget -O - https://github.com/carstene1ns/libgxflux/archive/0a636b8fd82052a17f1bc15d2a5e3b5f65bde3e6.tar.gz |tar zxf -
	cd libgxflux*/
	DEVKITPRO=/opt/devkitpro DEVKITPPC=$prefix do_make
fi
