do_fetch
do_configure --disable-thorough-tests
# We do not need these tests or these examples and depending on how the compiler
# was set up (like the Android compiler) they may fail to link properly even
# though the libraries were built fine
echo "all install clean:" > src/test_libFLAC++/Makefile
echo "all install clean:" > examples/Makefile
do_make
