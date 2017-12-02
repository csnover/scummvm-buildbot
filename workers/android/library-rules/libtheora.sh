do_fetch

# libtheora has an outdated autotools config which does not know of androideabi,
# so replace it with a new one
dh_update_autotools_config

do_configure --disable-spec --disable-examples
do_make -C lib
do_make -C include
make install-pkgconfigDATA
