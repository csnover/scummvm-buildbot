do_fetch

# glib will generate a DllMain even if it is a statical library, which we do not
# want since it will cause duplicate symbol errors during linking. This patch is
# from https://github.com/Alexpux/MINGW-packages/blob/master/mingw-w64-glib2/0004-glib-prefer-constructors-over-DllMain.patch
patch -p1 < ../glib2.0-no-dllmain.patch

do_configure --with-threads=win32 --with-pcre=internal

make -j$num_cpus -C glib/gnulib
make -j$num_cpus -C glib/libcharset
make -j$num_cpus -C glib/pcre
make -j$num_cpus -C glib \
	install-binSCRIPTS \
	install-libLTLIBRARIES \
	install-deprecatedincludeHEADERS \
	install-glibincludeHEADERS \
	install-glibsubincludeHEADERS \
	install-nodist_configexecincludeHEADERS
make -j$num_cpus -C gthread \
	install-libLTLIBRARIES
# Technically we should probably compile gio, gmodule, and gobject too, but
# FluidSynth does not use these, so whatever, let’s go crazy and save some
# compiler time and disk space!
make install-pkgconfigDATA
