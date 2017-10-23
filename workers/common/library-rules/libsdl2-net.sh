do_fetch
do_configure
# showinterfaces.c indirectly includes SDL_main.h which #defines main to
# SDL_main when __ANDROID__ is defined, so it won't compile in the usual manner,
# so just stub it out
echo 'int main(){return 0;}' > showinterfaces.c
do_make
