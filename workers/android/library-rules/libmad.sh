get_dependencies automake debhelper libtool quilt
do_fetch

# Unlike the other packages, for some reason libmad does not
# auto-apply quilt patches from the debian directory, which are
# needed to (among other things) avoid compilation failures due to
# the use of a flag `-fforce-mem`` which was removed in GCC 4.3.
dh_quilt_patch

# libmad has an outdated autotools config which does not know of androideabi,
# so replace it with a new one
dh_update_autotools_config

touch NEWS AUTHORS ChangeLog
autoreconf -i

do_configure
make -j$num_cpus install-libLTLIBRARIES install-includeHEADERS
