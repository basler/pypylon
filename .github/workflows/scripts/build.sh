#!/bin/bash
set -e

usage()
{
    echo "Usage: $0 [<options>]"
    echo "Options:"
    echo "  --python <path to binary>                 Use the given python binary"
    echo "  --update-platform-tag <platform-tag>      Use auditwheel repair to set the platform tag"
    echo "  --disable-tests                           Disable automatic unittests"
    echo "  -h                                        This usage help"
}

PYTHON="python"
DISABLE_TESTS=""
UPDATE_PLATFORM_TAG=""

# parse args
while [ $# -gt 0 ]; do
    arg="$1"
    case $arg in
        --python) PYTHON="$2" ; shift ;;
        --update-platform-tag) UPDATE_PLATFORM_TAG="$2"; shift ;;
        --disable-tests) DISABLE_TESTS=1 ;;
        -h|--help) usage ; exit 1 ;;
        *)         echo "Unknown argument $arg" ; usage ; exit 1 ;;
    esac
    shift
done

BASEDIR="$(cd $(dirname $0)/../.. ; pwd)"
#enter source dir
pushd $BASEDIR

BUILD_DIR="build-dockerized-$(date +%s)"

if [ -d "$BUILD_DIR" ]; then
    echo "Build dir $BUILD_DIR already exists. Abort."
    exit 1
fi
mkdir -p $BUILD_DIR

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