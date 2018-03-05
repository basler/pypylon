#!/bin/bash
set -e
#This is a rather hacky script to build pypylon for the current architecture.
#it automatically searches and extracts the correct sdk from the directory given by $1
#this is needed for the jenkins build
#if you want to build pyplon for your installed pylon, don't use this script. You can do:
# PYLON_ROOT=/path/to/your/pylon/install python3 setup.py bdist_wheel

if [ $# -ne 1 ]; then
	echo "Call this script with $0 <dir to the pylon SDK tar.gz files>"
	exit 1
fi

SDK_FILES_DIR=`readlink -f $1`

cd `dirname $0`/..
BUILD_DIR=${BUILD_DIR:-`pwd`/linux-build}

#guess architecture
ARCH=`uname -m`
case "$ARCH" in
	i?86) BUILD=x86 ;;
	x86_64) BUILD=x86_64 ;;
	armel) BUILD=armel ;;
	armhf) BUILD=armhf ;;
	arm*)
		BUILD=armel
		if [ -d /lib/arm-linux-gnueabihf ]; then
			BUILD=armhf
		fi
		;;
	aarch64) BUILD=arm64 ;;
esac

#rm -r $BUILD_DIR
mkdir -p $BUILD_DIR

#check if we need to extract the SDK
if [ ! -d $BUILD_DIR/pylon5-$BUILD ]; then
(
	cd $BUILD_DIR
	tar -xzf $SDK_FILES_DIR/pylonSDK-*-$BUILD.tar.gz
	mv pylon5 pylon5-$BUILD
)
fi

#we always use the extracted SDK, if you need this script to build against your pylon version add the logic :-)
PYLON_ROOT=$BUILD_DIR/pylon5-$BUILD
echo "Using pylon SDK from $PYLON_ROOT"
export PYLON_ROOT

python3 setup.py clean
python3 setup.py bdist_wheel
