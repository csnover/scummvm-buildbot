do_fetch
# libpng unconditionally compiles some tools which try to link to
# interfaces that do not exist on GC/Wii. There is no flag to
# disable these compilations, so just empty out the affected tool
# for now.
echo "int main() { return 0; }" > contrib/tools/pngcp.c
do_configure
do_make
