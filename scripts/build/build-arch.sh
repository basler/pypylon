#!/bin/bash
set -e

THISDIR="$(cd $(dirname $0) ; pwd)"
BASEDIR="$(cd $(dirname $0)/../..; pwd)"

#https://www.python.org/dev/peps/pep-0425/

usage()
{
    echo "Usage: $0 [<options>]"
    echo "Options:"
    echo "  --pylon-dir <name>            Directory where to look for pylon installers. This script then tries to find the correct one. This is not needed, if pylon-base is given"
    echo "  --platform-tag <name>         The python platform tag to build"
    echo "  --abi-tag <package>           The python abi tag to build"
    echo "  --disable-tests               Disable automatic unittests"
    echo "  --drop-to-shell               Drop into an interactive bash inside the container for debugging purposes"
    echo "  -h                            This usage help"
}

ABI_TAG=""
PLATFORM_TAG=""
PYLON_TGZ_DIR=""
PYLON_DIR=""
DISABLE_TESTS=""
DROP_TO_SHELL=""

while [ $# -gt 0 ]; do
    arg="$1"
    case $arg in
        --pylon-dir) PYLON_DIR="$2" ; shift ;;
        --platform-tag) PLATFORM_TAG="$2" ; shift ;;
        --abi-tag) ABI_TAG="$2" ; shift ;;
        --disable-tests) DISABLE_TESTS=1 ;;
        --drop-to-shell) DROP_TO_SHELL=1 ;;
        -h|--help) usage ; exit 1 ;;
        *)         echo "Unknown argument $arg" ; usage ; exit 1 ;;
    esac
    shift
done

BASE_IMAGE=""
BASE_IMAGE32=""
BASE_IMAGE64=""
QEMU_ARCH=""
PYTHON="python"
PYLON_ARCH=""
PYLON=""

BUILD_DISTRO="debian"
if [[ $PLATFORM_TAG =~ manylinux2014* ]]; then
    BUILD_DISTRO="manylinux"
fi

if [ $BUILD_DISTRO = "debian" ]; then

    #Note: Be careful when changing the base image. Not every image is available for every architecture.
    case $ABI_TAG in
        cp36m)  BASE_IMAGE32="python:3.6.15-buster";   BASE_IMAGE64="python:3.6.15-bullseye" ;;
        cp37m)  BASE_IMAGE32="python:3.7.16-buster";   BASE_IMAGE64="python:3.7.16-bullseye" ;;
        cp38)   BASE_IMAGE32="python:3.8.16-buster";   BASE_IMAGE64="python:3.8.16-bullseye" ;;
        cp39)   BASE_IMAGE32="python:3.9.16-buster";   BASE_IMAGE64="python:3.9.16-bullseye" ;;
        cp3_10) BASE_IMAGE32="python:3.10.11-buster";  BASE_IMAGE64="python:3.10.11-bullseye" ;;
        cp3_11) BASE_IMAGE32="python:3.11.3-buster";   BASE_IMAGE64="python:3.11.3-bullseye" ;;
        cp3_12) 				       BASE_IMAGE64="python:3.12.4-bullseye" ;;
        cp3_13) 				       BASE_IMAGE64="python:3.13.0-bullseye" ;;
        *)
        echo "Unsupported abi '$ABI_TAG'. Supported tags: cp36m, cp37m, cp38, cp39, cp3_10, cp3_11, cp3_12, cp3_13"
        exit 1
    esac
else
    #Note: Be careful when changing the base image. Not every image is available for every architecture.
    case $ABI_TAG in
        cp36m) PYTHON="/opt/python/cp36-cp36m/bin/python" ;;
        cp37m) PYTHON="/opt/python/cp37-cp37m/bin/python" ;;
        cp38) PYTHON="/opt/python/cp38-cp38/bin/python" ;;
        cp39) PYTHON="/opt/python/cp39-cp39/bin/python" ;;
        *)
        echo "Unsupported manylinux abi '$ABI_TAG'. Supported tags: cp36m, cp37m, cp38, cp39"
        exit 1
    esac
fi

# When running a armv7 container on a native aarch64 machine, uname -a still outputs aarch64 instead of armv7
# Python assumes it should buid for aarch64. Wrapping everything with linux32 fixes the issue.
# linux64 is the default
CMD_WRAPPER=linux64

case $PLATFORM_TAG in
    linux_x86_64)           QEMU_ARCH="x86_64";   BASE_IMAGE="amd64/$BASE_IMAGE64";                 DOCKER_PLATFORM="linux/amd64";   PYLON_ARCH=x86_64 ;;
    linux_i686)             QEMU_ARCH="i386";     BASE_IMAGE="i386/$BASE_IMAGE32";                  DOCKER_PLATFORM="linux/i386";    PYLON_ARCH=x86 ;        CMD_WRAPPER=linux32 ;;
    linux_armv7l)           QEMU_ARCH="arm";      BASE_IMAGE="arm32v7/$BASE_IMAGE32";               DOCKER_PLATFORM="linux/arm/v7";  PYLON_ARCH=armhf        CMD_WRAPPER=linux32 ;;
    linux_aarch64)          QEMU_ARCH="aarch64";  BASE_IMAGE="arm64v8/$BASE_IMAGE64";               DOCKER_PLATFORM="linux/arm64";   PYLON_ARCH=aarch64 ;;
    manylinux_2_31_x86_64)  QEMU_ARCH="x86_64";   BASE_IMAGE="amd64/$BASE_IMAGE64";                 DOCKER_PLATFORM="linux/amd64";   PYLON_ARCH=x86_64 ;;
    manylinux_2_28_i686)    QEMU_ARCH="i386";     BASE_IMAGE="i386/$BASE_IMAGE32";                  DOCKER_PLATFORM="linux/i386";    PYLON_ARCH=x86 ;        CMD_WRAPPER=linux32 ;;
    manylinux_2_28_armv7l)  QEMU_ARCH="arm";      BASE_IMAGE="arm32v7/$BASE_IMAGE32";               DOCKER_PLATFORM="linux/arm/v7";  PYLON_ARCH=armhf        CMD_WRAPPER=linux32 ;;
    manylinux_2_31_aarch64) QEMU_ARCH="aarch64";  BASE_IMAGE="arm64v8/$BASE_IMAGE64";               DOCKER_PLATFORM="linux/arm64";   PYLON_ARCH=aarch64 ;;
    manylinux2014_x86_64)   QEMU_ARCH="x86_64";   BASE_IMAGE="quay.io/pypa/manylinux2014_x86_64";   DOCKER_PLATFORM="linux/amd64";   PYLON_ARCH=x86_64 ;;
    manylinux2014_i686)     QEMU_ARCH="i386";     BASE_IMAGE="quay.io/pypa/manylinux2014_i686";     DOCKER_PLATFORM="linux/i386";    PYLON_ARCH=x86 ;        CMD_WRAPPER=linux32 ;;
    manylinux2014_aarch64)  QEMU_ARCH="aarch64";  BASE_IMAGE="quay.io/pypa/manylinux2014_aarch64";  DOCKER_PLATFORM="linux/arm64";   PYLON_ARCH=aarch64 ;;
    *)
    echo "Unsupported platform tag '$PLATFORM_TAG'. Supported platforms: linux_x86_64, linux_i686, linux_armv7l, linux_aarch64, manylinux2014_x86_64, manylinux2014_i686, manylinux2014_aarch64, manylinux_2_28_<arch>, manylinux_2_31_<arch>"
    exit 1
esac


if [ -z "$PYLON_DIR" ]; then
    echo "pylon-dir must be given"
    exit 1
fi

#test for pylon 6.1
files=( $PYLON_DIR/pylon-*-${PYLON_ARCH}_setup.tar.gz )
PYLON="${files[0]}"

if [ ! -f "$PYLON" ]; then
    echo "Couldn't find pylon installer in $PYLON_DIR"
    exit 1
fi

DOCKER_TAG="pypylon-$PLATFORM_TAG-$(date +%s)"
docker build --network host \
  --platform "$DOCKER_PLATFORM" \
  --build-arg "QEMU_TARGET_ARCH=$QEMU_ARCH" \
  --build-arg "DOCKER_BASE_IMAGE=$BASE_IMAGE" \
  --build-arg "CMD_WRAPPER=$CMD_WRAPPER" \
  --tag "$DOCKER_TAG" - < $THISDIR/Dockerfile.$BUILD_DISTRO


#make path absolute
PYLON_TGZ=$(readlink -m "$PYLON" || true)

#strip basedir from filename
#this allows us to easiliy mount the tgz to a given destination inside the container
PYLON_TGZ_BASE=$(basename $PYLON_TGZ)


ARGS=""
if [ -n "$DISABLE_TESTS" ]; then
    ARGS="$ARGS --disable-tests"
fi

if [[ $PLATFORM_TAG =~ manylinux* ]]; then
    ARGS="$ARGS --update-platform-tag $PLATFORM_TAG"
fi

if [ -z "$DROP_TO_SHELL" ]; then 
    docker run -v "$BASEDIR:/work" -v "$PYLON_TGZ:/$PYLON_TGZ_BASE" --user $(id -u) $DOCKER_TAG  /work/scripts/build/build.sh --pylon-tgz "/$PYLON_TGZ_BASE" --python "$PYTHON" $ARGS
else
    MSG="In a normal build this script would run: /work/scripts/build/build.sh --pylon-tgz \"/$PYLON_TGZ_BASE\" --python \"$PYTHON\" $ARGS"
    exec docker run -ti -v "$BASEDIR:/work" -v "$PYLON_TGZ:/$PYLON_TGZ_BASE" --user $(id -u) $DOCKER_TAG bash -c "echo '$MSG'; exec bash"
fi
