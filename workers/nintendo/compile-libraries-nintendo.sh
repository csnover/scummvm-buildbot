#!/usr/bin/env bash

./compile-libraries.sh powerpc-eabi /opt/devkitpro/devkitPPC $@

nds_flags="-march=armv6k -mtune=mpcore -mfloat-abi=hard"
CPPFLAGS=$nds_flags LDFLAGS=$nds_flags ./compile-libraries.sh arm-none-eabi /opt/devkitpro/devkitARM $@
