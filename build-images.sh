#!/usr/bin/env bash

buildbot_version=0.9.12

docker build . -t scummvm-buildbot-master
root_dir=$(pwd)
for dockerfile in $(find workers -name Dockerfile); do
    worker_dir=$(dirname $dockerfile)
    cd "$worker_dir"
    worker_name=$(basename $worker_dir)
    docker build . -t scummvm-buildbot-$worker_name --build-arg BUILDBOT_VERSION=$buildbot_version
    cd "$root_dir"
done
