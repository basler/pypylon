#!/bin/bash
set -e

THISDIR="$(cd $(dirname $0) ; pwd)"

#https://www.python.org/dev/peps/pep-0425/

usage()
{
    echo "Usage: $0 [<options>]"
    echo "Options:"
    echo "  --pylon-base <name>           Base to get the pylon installer name. Something like ./installer/pylon-5.0.12.11829 This script will add -<arch>.tar.gz"
    echo "  --pylon-dir <name>            Directory where to look for pylon installers. This script then tries to find the correct one. This is not needed, if pylon-base is given"
    echo "  --platform-tag <name>         The python platform tag to build"
    echo "  --abi-tag <package>           The python abi tag to build"
    echo "  -h                            This usage help"
}

ABI_TAG=""
PLATFORM_TAG=""
PYLON_TGZ_DIR=""
PYLON_BASE=""
PYLON_DIR=""

while [ $# -gt 0 ]; do
    arg="$1"
    case $arg in
        --pylon-base) PYLON_BASE="$2" ; shift ;;
        --pylon-dir) PYLON_DIR="$2" ; shift ;;
        --platform-tag) PLATFORM_TAG="$2" ; shift ;;
        --abi-tag) ABI_TAG="$2" ; shift ;;
        -h|--help) usage ; exit 1 ;;
        *)         echo "Unknown argument $arg" ; usage ; exit 1 ;;
    esac
    shift
done

BASE_IMAGE=""
QEMU_ARCH=""
PYTHON="python"
PYLON_ARCH=""
PYLON=""

case $ABI_TAG in
    cp34m) BASE_IMAGE="python:3.4.8-wheezy" 
        case $PLATFORM_TAG in 
            linux_aarch64) BASE_IMAGE="python:3.4.8-jessie" ;;
        esac
        ;;
    cp35m) BASE_IMAGE="python:3.5.5-jessie" ;;
    cp36m) BASE_IMAGE="python:3.6.5-jessie" ;;
    *)
    echo "Unsupported abi '$ABI_TAG'"
    exit 1
esac

case $PLATFORM_TAG in
    linux_x86_64)  QEMU_ARCH="x86_64";  BASE_IMAGE="amd64/$BASE_IMAGE";   PYLON_ARCH=x86_64 ;;
    linux_i686)    QEMU_ARCH="i386";    BASE_IMAGE="i386/$BASE_IMAGE";    PYLON_ARCH=x86 ;;
    linux_armv7l)  QEMU_ARCH="arm";     BASE_IMAGE="arm32v7/$BASE_IMAGE"; PYLON_ARCH=armhf ;;
    linux_aarch64) QEMU_ARCH="aarch64"; BASE_IMAGE="arm64v8/$BASE_IMAGE"; PYLON_ARCH=arm64 ;;
    manylinux1_*) echo "manylinux is not yet supported :-("; exit 1 ;;
    *)
    echo "Unsupported platform tag '$ABI_TAG'"
    exit 1
esac

if [ -n "$PYLON_DIR" ]; then
    pattern="*.txt"
    files=( $PYLON_DIR/pylon-*-$PYLON_ARCH.tar.gz )
    PYLON="${files[0]}"
    if [ ! -f "$PYLON" ]; then
        echo "Couldn't find pylon installer in $PYLON_DIR"
        exit 1
    fi
else
    PYLON=$PYLON_BASE-$PYLON_ARCH.tar.gz
    if [ ! -f "$PYLON" ]; then
        echo "Pylon installer $PYLON doesn't exist"
        exit 1
    fi
fi


echo "build-with-docker.sh --qemu-target-arch $QEMU_ARCH --docker-base-image $BASE_IMAGE --python $PYTHON --pylon-tgz $PYLON"
$THISDIR/build-with-docker.sh --qemu-target-arch $QEMU_ARCH --docker-base-image $BASE_IMAGE --python $PYTHON --pylon-tgz $PYLON