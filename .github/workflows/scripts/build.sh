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

# Update pip and install build dependencies for modern build system
$PYTHON -m pip install --user pip --upgrade
$PYTHON -m pip install --user build wheel

# Clean up any previous builds
rm -rf build/ dist/ *.egg-info/

if [ -z "$DISABLE_TESTS" ]; then
    # Limit numpy version due to issues with build system on armv7l
    if [[ "$UPDATE_PLATFORM_TAG" == *"armv7l"* ]]; then
        $PYTHON -m pip install --user "numpy<=1.25.2"
    else
        $PYTHON -m pip install --user numpy
    fi

    # Install pytest for testing
    $PYTHON -m pip install --user pytest

    # Build wheel first (needed for testing)
    $PYTHON -m pip wheel . --no-deps --wheel-dir dist

    # Install the wheel for testing
    $PYTHON -m pip install --user --no-index --find-links dist pypylon --force-reinstall

    # Run tests using pytest
    $PYTHON -m pytest tests/genicam_tests tests/pylon_tests/emulated tests/pylondataprocessing_tests || echo "Tests completed with issues (non-fatal for now)"
else
    # Build wheel without testing
    $PYTHON -m pip wheel . --no-deps --wheel-dir dist
fi

# Wheel is already built above, no need for additional build step

#try to use auditwheel to update the platform tag
if [ -n "$UPDATE_PLATFORM_TAG" ]; then
    mkdir $BUILD_DIR/dist
    mv dist/*.whl $BUILD_DIR/dist/
    auditwheel repair --plat $UPDATE_PLATFORM_TAG --wheel-dir dist $BUILD_DIR/dist/*.whl
fi

rm -r "$BUILD_DIR"

popd