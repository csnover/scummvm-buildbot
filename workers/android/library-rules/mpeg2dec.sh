get_dependencies automake libtool
do_fetch
rm -rf .auto
dh_update_autotools_config
autoreconf -i
do_configure
do_make
