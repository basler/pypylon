#!/bin/bash
set -e

usage()
{
    echo "Usage: $0 [<options>]"
    echo "Options:"
    echo "  --pylon-tgz <package>      Use the given pylon installer tgz"
    echo "  --python <path to binary>  Use the given python binary"
    echo "  -h                         This usage help"
}

PYLON_TGZ=""
PYTHON="python"

# parse args
while [ $# -gt 0 ]; do
    arg="$1"
    case $arg in
        --pylon-tgz) PYLON_TGZ="$2" ; shift ;;
        --python) PYTHON="$2" ; shift ;;
        -h|--help) usage ; exit 1 ;;
        *)         echo "Unknown argument $arg" ; usage ; exit 1 ;;
    esac
    shift
done

if [ ! -e "$PYLON_TGZ" ]; then
    echo "Pylon installer '$PYLON_TGZ' doesn't exist"
    exit 1
fi

#make path absolute
PYLON_TGZ=$(readlink -m "$PYLON_TGZ")

BASEDIR="$(cd $(dirname $0)/../.. ; pwd)"
#enter source dir
pushd $BASEDIR

BUILD_DIR="build-dockerized-$(date +%s)"

if [ -d "$BUILD_DIR" ]; then
    echo "Build dir $BUILD_DIR already exists. Abort."
    exit 1
fi

#rm -r $BUILD_DIR
mkdir -p $BUILD_DIR
pushd $BUILD_DIR
tar -xzf $PYLON_TGZ
#now we have the extracted outer tar
tar -xzf pylon-*/pylonSDK-*.tar.gz
#now there is a pylon5 dir
popd

#we always use the extracted SDK, if you need this script to build against your pylon version add the logic :-)
PYLON_ROOT=$BUILD_DIR/pylon5
echo "Using pylon SDK from $PYLON_ROOT"
export PYLON_ROOT

$PYTHON setup.py clean
$PYTHON setup.py bdist_wheel

rm -r "$BUILD_DIR"

popd


