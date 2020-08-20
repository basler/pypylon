#!/bin/bash
set -e

usage()
{
    echo "Usage: $0 [<options>]"
    echo "Options:"
    echo "  --pylon-tgz <package>                     Use the given pylon installer tgz"
    echo "  --python <path to binary>                 Use the given python binary"
    echo "  --update-platform-tag <platform-tag>      Use auditwheel repair to set the platform tag"
    echo "  --disable-tests                           Disable automatic unittests"
    echo "  -h                                        This usage help"
}

PYLON_TGZ=""
PYTHON="python"
DISABLE_TESTS=""
UPDATE_PLATFORM_TAG=""

# parse args
while [ $# -gt 0 ]; do
    arg="$1"
    case $arg in
        --pylon-tgz) PYLON_TGZ="$2" ; shift ;;
        --python) PYTHON="$2" ; shift ;;
        --update-platform-tag) UPDATE_PLATFORM_TAG="$2"; shift ;;
        --disable-tests) DISABLE_TESTS=1 ;;
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
mkdir -p $BUILD_DIR/pylon
pushd $BUILD_DIR/pylon
tar -xzf $PYLON_TGZ

# cope with different pylon tarball structures
if [ -f pylon*.tar.gz ]; then #pylon 6.1 structure
    tar -xzf pylon*.tar.gz
    PYLON_ROOT=$BUILD_DIR/pylon
elif [ -d bin ]; then #the pylon 6.0 nightly that was released for dart-mipi didn't contain an second tarball
    PYLON_ROOT=$BUILD_DIR/pylon
elif [ -f pylon-*/pylonSDK-*.tar.gz ]; then # pylon < 6
     #extract the inner tar from pylon 5
    tar -xzf pylon-*/pylonSDK-*.tar.gz
    PYLON_ROOT=$BUILD_DIR/pylon/pylon5
else
    echo "Failed to detect and extract the pylon version."
    exit 1
fi

popd

echo "Using pylon SDK from $PYLON_ROOT"
export PYLON_ROOT

$PYTHON setup.py clean

if [ -z "$DISABLE_TESTS" ]; then
    $PYTHON -m pip install --user numpy
    #For now failed tests are accepted until all are fixed
    $PYTHON setup.py test
fi

$PYTHON setup.py bdist_wheel

#try to use auditwheel to update the platform tag
if [ -n "$UPDATE_PLATFORM_TAG" ]; then
    mkdir $BUILD_DIR/dist
    mv dist/*.whl $BUILD_DIR/dist/
    auditwheel repair --plat $UPDATE_PLATFORM_TAG --wheel-dir dist $BUILD_DIR/dist/*.whl
fi

rm -r "$BUILD_DIR"

popd


