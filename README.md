# ScummVM Buildbot

This Buildbot uses [Docker](https://www.docker.com/).

The buildmaster’s configuration is in `master`, with a stub `master.cfg` in the
root (due to limitations of Docker, and the desire to keep workers encapsulated
in the `workers` subdirectory).

Individual worker configurations are in `workers` subdirectories.

## Features

* Each cross-compiler has its own separate worker image and configuration, so
  can be maintained and updated independently of the rest of the build system
* Failed builders are given top priority for any new builds
* Newer builds are given priority over older queued builds
* Authentication for manual builds, rebuilds, and build cancelling uses GitHub
  for login
* Successful builds are automatically packaged and uploaded for immediate
  consumption
* Workers may optionally share a single Git repository
* Builds automatically scale across all available CPU cores

## Building images

The buildmaster’s `Dockerfile` is in the root. Each worker’s `Dockerfile` is in
its own subdirectory in `workers`.

Run the provided `build-images.sh` script to build images from source. Run
`build-images.sh --help` for usage information.

## Configuring Buildbot

All normally configurable options for the buildmaster are exposed in the
`docker-compose.yml` file, which is used to deploy the build system.

When making changes to the buildmaster, configurable options should be exposed
to `docker-compose` in a similar manner, rather than being hard-coded into the
buildmaster’s Python code.

Secret keys for the buildmaster should be set in a `secrets.cfg` file next to
the `master.cfg` file in the root. The secret file is a Python module with these
keys:

* `github_client_id`: The client ID for the ScummVM OAuth app on GitHub that is
  used for authentication.
* `github_client_secret`: The client secret for the ScummVM OAuth app on GitHub
  that is used for authentication.
* `github_hook_secret`: The secret string used by the GitHub Web hook.
* `irc_password`: The nickserv password for the IRC status bot.
* `worker_password`: The password used by workers when connecting to the
  buildmaster.

## Deploying

Run `docker-compose up -d` after building images to stand up the Buildbot
cluster.

## Upgrading Buildbot

Change the version number in the buildmaster’s `Dockerfile` to upgrade Buildbot.
Worker images will also use this version when you generate images with
`build-images.sh`.

## Adding new workers

* Create a new directory in `workers`. The name of the directory will be used as
  the name of the worker.
* Copy template files from `workers/_template` to the new worker’s subdirectory.
* Edit the copied files appropriately. The `Dockerfile` should install the
  cross-compiler and ScummVM dependencies for the target platform, the Buildbot
  worker and its dependencies, and configure the environment’s `PATH`
  appropriately for the cross-compiler. Please take care to delete any temporary
  files and caches generated during package installation or toolchain building
  at the end of each `RUN` command.
* Run `build-images.sh <worker name>` to rebuild the master image and the new
  worker image.
* Add the new worker to the `docker-compose.yml` file, following the pattern
  used by existing workers already in the file.
