#!/usr/bin/env bash
set -e

if [ $# -lt 1 ]; then
	echo "Usage: $0 path/to/Xcode.app"
	echo
	echo "To get Xcode.app, you will need an Apple Developer Account."
	echo "Go to <https://developer.apple.com/devcenter/download.action?path=%2FDeveloper_Tools%2Fxcode_5.1.1%2Fxcode_5.1.1.dmg>"
	echo "to log in and download Xcode 5.1.1."
	exit 1
fi

if [ ! -d $1 ]; then
	echo "$1 is not a readable directory"
	exit 1
fi

out=$(dirname $0)
sdk_dir="$1/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS7.1.sdk"
cxx_headers_dir="$1/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/c++/v1"

if [ ! -d $sdk_dir ]; then
	echo "Could not find SDK directory at $1"
	exit 1
fi

if [ ! -d $cxx_headers_dir ]; then
	echo "Could not find C++ headers directory at $1"
fi

echo "Copying iPhoneOS7.1.sdk..."
cp -a "$sdk_dir" "$out"
cp -a "$cxx_headers_dir" "$out/iPhoneOS7.1.sdk/usr/include/c++"
if which xattr >/dev/null 2>&1; then
	echo "Clearing quarantine flags..."
	xattr -dr com.apple.quarantine "$out/iPhoneOS7.1.sdk"
fi
echo "Creating iPhoneOS7.1.sdk.tar.gz..."
tar --options gzip:compression-level=0 -C "$out" -czf "$out/iPhoneOS7.1.sdk.tar.gz" iPhoneOS7.1.sdk
echo "Cleaning up..."
rm -r iPhoneOS7.1.sdk
echo "Done"
