get_dependencies automake libtool
do_fetch
rm -rf .auto
dh_update_autotools_config
autoreconf -i
# mpeg2dec includes non-PIC ARM assembly which is forbidden in Android 23+, so
# disable it from being used
sed -i 's/arm\*)/xxarmxx)/' configure
do_configure
do_make
