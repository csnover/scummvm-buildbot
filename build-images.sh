#!/usr/bin/env bash
set -e

usage () {
    echo "Usage: $0 [--help] [--no-master] [<worker name>|all] [<worker name> ...]"
    echo
    echo "Builds the Docker images used for ScummVM Buildbot."
    echo
    echo "Pass no worker names to build only the master image. Pass \"all\" as"
    echo "the worker name to build the master image plus all worker images."
    echo "Otherwise, pass the names of the worker images you want to build."
    echo
    echo "--no-master: Build only the specified worker images"
}

build_worker () {
    local worker_dir=$1
    local worker_name=$(basename $worker_dir)
    cd "$worker_dir"
    echo "Building worker $worker_name"
    docker build . -t "scummvm-buildbot-$worker_name" \
        --build-arg "BUILDBOT_VERSION=$buildbot_version"
    cd "$root_dir"
}

if [ $# -gt 0 -a "$1" == "--help" ]; then
    usage
    exit 0
fi

build_master=1
if [ $# -gt 0 -a "$1" == "--no-master" ]; then
    build_master=0
    shift
fi

buildbot_version=$(sed -n 's/FROM.*buildbot-master:v\{0,1\}\([^[:space:]]\)/\1/p' Dockerfile)
root_dir=$(pwd)

if [ -z $buildbot_version ]; then
    echo "Could not find Buildbot version from master Dockerfile"
    exit 1
fi

if [ $build_master -eq 1 ]; then
    echo "Building master image"
    docker build . -t scummvm-buildbot-master
fi

if [ $# -gt 0 ]; then
    if [ "$1" == "all" ]; then
        echo "Building all workers"
        for dockerfile in $(find workers -name Dockerfile); do
            worker_dir=$(dirname $dockerfile)
            build_worker $worker_dir
        done
    else
        for worker_name in $@; do
            worker_dir="workers/$worker_name"
            if [ ! -d $worker_dir ]; then
                echo "Worker $worker_name does not exist"
            elif [ ! -f "$worker_dir/Dockerfile" ]; then
                echo "Worker $worker_name has no Dockerfile"
            else
                build_worker "workers/$worker_name"
            fi
        done
    fi
fi
