#!/bin/bash
set -e

THISDIR="$(cd $(dirname $0); pwd)"
BASEDIR="$(cd $(dirname $0)/../..; pwd)"

usage()
{
    echo "Usage: $0 [<options>]"
    echo "Options:"
    echo "  --docker-base-image <name>    The docker image used to build"
    echo "  --qemu-target-arch  <name>    The arch part of qemu-<arch>-static"
    echo "  --pylon-tgz <package>         Use the given tgz"
    echo "  --python <path to python bin> Use the given python for the build"
    echo "  -h                            This usage help"
}

PYLON_TGZ=""
PYTHON="python"
DOCKER_BASE_IMAGE=""
PROXY="$HTTP_PROXY"
QEMU_TARGET_ARCH=""

# parse args
while [ $# -gt 0 ]; do
    arg="$1"
    case $arg in
        --docker-base-image) DOCKER_BASE_IMAGE="$2"; shift ;;
        --qemu-target-arch) QEMU_TARGET_ARCH="$2"; shift ;;
        --pylon-tgz) PYLON_TGZ="$2" ; shift ;;
        --python) PYTHON="$2" ; shift ;;
        -h|--help) usage ; exit 1 ;;
        *)         echo "Unknown argument $arg" ; usage ; exit 1 ;;
    esac
    shift
done

#make path absolute
PYLON_TGZ=$(readlink -m "$PYLON_TGZ")

if [[ "$PYLON_TGZ" != "$BASEDIR"* ]]; then
    echo "Pylon installer must be contained in '$BASEDIR'."
    exit 1
fi

#strip basedir from filename
DOCKER_PYLON_TGZ=${PYLON_TGZ#"$BASEDIR/"}
PYLON_TGZ_BASE=$(basename $PYLON_TGZ)


cd $THISDIR

DOCKER_TAG="pypylon-$(date +%s)"
docker build --build-arg "HTTP_PROXY=$HTTP_PROXY" \
                --build-arg "http_proxy=$HTTP_PROXY" \
                --build-arg "HTTPS_PROXY=$HTTPS_PROXY" \
                --build-arg "https_proxy=$HTTPS_PROXY" \
                --build-arg "QEMU_TARGET_ARCH=$QEMU_TARGET_ARCH" \
                --build-arg "DOCKER_BASE_IMAGE=$DOCKER_BASE_IMAGE" \
                --tag "$DOCKER_TAG" .

set -x
docker run -v "$BASEDIR:/work" -v "$PYLON_TGZ:/$PYLON_TGZ_BASE" --user $(id -u) $DOCKER_TAG  /work/scripts/build/build.sh --pylon-tgz "/$PYLON_TGZ_BASE" --python "$PYTHON"
#to debug issues with docker use the following line to jump into an interactive session
#exec docker run -ti -v "$BASEDIR:/work" -v "$PYLON_TGZ:/$PYLON_TGZ_BASE" $DOCKER_TAG  bash

        