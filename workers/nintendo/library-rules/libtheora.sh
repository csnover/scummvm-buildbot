do_fetch
# Theora tries to build some XML docs even when it can't, and this
# breaks the build, so just disable that by overwriting the doc
# Makefile.
echo "all install clean:" > doc/Makefile.am
echo "all install clean:" > doc/Makefile.in
do_configure --disable-spec --disable-examples
do_make
