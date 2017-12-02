# ScummVM Buildbot

This Buildbot uses [Docker](https://www.docker.com/).

The buildmaster’s configuration is in `master`. Individual worker configurations
are in `workers` subdirectories.

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
* Debug symbols may be split into their own separate archives during packaging
* Builds automatically scale across all available CPU cores

## Requirements

* A [copy of Docker 17.09+](https://www.docker.com/community-edition) (and
  `docker-compose` if you are getting Docker from a package manager)
* A clone of this repository
* Some patience

## Quick start

* Clone this repository
* Create a `secrets.cfg` in the root:

  ```python
  github_hook_secret = None
  worker_password = "worker"
  ```

* Run `docker-compose up -d`
* Go to http://localhost:28453/ in your browser
* To control builds from the UI, the login credentials (when in the default
  development mode) are `user`/`pass`

## Building images

**You do not need to build images from source if you are only wanting to run a
worker. Just run `docker-compose up -d buildbot-whatever`, which will fetch the
prebuilt image for the worker from Docker Hub.**

The buildmaster’s `Dockerfile` is in `master`. Each worker’s `Dockerfile` is in
its own subdirectory in `workers`.

Run the provided `build-images.sh` script to build images from source. Run
`build-images.sh --help` for usage information.

## Configuring Buildbot

All normally configurable options for the buildmaster are exposed in the
`docker-compose.yml` file, which is used to deploy the build system.

When making changes to the buildmaster, configurable options should be exposed
to `docker-compose` in a similar manner, rather than being hard-coded into the
buildmaster’s Python code.

Secret keys for the buildmaster should be set in a `secrets.cfg` file in the
root. The secret file is a Python module with these keys:

* `github_client_id`: The client ID for the ScummVM OAuth app on GitHub that is
  used for authentication.
* `github_client_secret`: The client secret for the ScummVM OAuth app on GitHub
  that is used for authentication.
* `github_hook_secret`: The secret string used by the GitHub Web hook.
* `irc_password`: The nickserv password for the IRC status bot.
* `worker_password`: The password used by workers when connecting to the
  buildmaster.

## Deploying

Run `docker-compose up -d`.

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

## Using workers as stand-alone compilers

* Create a `docker-compose.override.yml` which overrides the worker you want to
  mess with so that you (1) expose the ScummVM code from your host machine, and
  (2) override the entrypoint so it starts a shell instead of starting the
  Buildbot worker:

  ```yaml
  services:
    buildbot-whatever:
      volumes:
        - /host/path/to/scummvm:/data/sharedrepo
        - /host/path/for/build/output:/buildbot
      entrypoint: /bin/bash
  ```

* Start a shell in the worker environment using
  `docker-compose run --rm buildbot-whatever`
* Run `/data/sharedrepo/configure`
* Run `make -j$(nproc)`

If you are stopping and restarting the worker a lot you may also want to bind
the `/data/ccache` directory of the container somewhere so that the compiler
cache persists across compiles, since this is where the compiler cache goes by
default.

## Tips for creating & debugging workers

* To run a test build, log in to Buildbot, click on Builds in the main menu,
  then Builders, then click on the builder you want to test, then click the
  “Run manual build” button in the top-right corner, enter a message, and click
  “Start Build”.
* Once you log in to the buildmaster, you can go to any Builder page to run a
  manual build, or to any build’s results page to cancel or re-run the same
  build. The buttons for these actions will appear at the top-right of the
  window, next to the avatar image.
* If you are creating a new worker based off an existing Docker Hub image, and
  want to inspect the base image first, run
  `docker run --rm -u0 <image-name> /bin/bash` to automatically download and
  start up a container for that image.
* If you need to compile some third-party libraries from source, take a look at
  the [common/compile-libraries.sh](./common/compile-libraries.sh) script. (The
  goal is to have one reusable, general-purpose script for the common operations
  involved in compiling third-party libraries.)
* Running `docker-compose up` without `-d` will send the logs of all the started
  containers’ main processes to the console so they can be viewed. It will also
  run the containers only until you hit Ctrl+C. Otherwise, you can view the logs
  for running services at any time with `docker-compose logs`.
* Every time a Docker container is stopped and restarted, any information not
  stored in a volume will be destroyed. So, if you want to inspect a directory
  of a container, consider binding it to your host filesystem by adding extra
  `volumes` to the worker’s configuration in `docker-compose.yml`:

  ```yaml
  volumes:
    <<: *defaultVolumes
    - /path/on/host:/path/in/container
  ```

* It is possible to execute another command on any running service. To do this,
  run `docker-compose exec <service-name> <command>`. This is particularly
  useful for spawning a shell to perform actions inside the container. If you
  want to run the command as root, add a `-u0` flag after `exec`. If you plan on
  doing something that requires privileged kernel access (e.g. `strace`), add
  the `--privileged` flag. If the main process exits, this process will also
  exit; to get around that, you might consider running `tail -f /dev/null` in
  the main process after an error condition.
* It is possible to start a service with a one-time override of the main
  command. To do this, run `docker-compose run <service-name> <command>`. To
  avoid creating junk containers every time you do this, add the `--rm` flag.
* After rebuilding your worker image, you will need to run
  `docker-compose stop <service-name> && docker-compose up <service-name>`
  instead of `docker-compose restart <service-name>` to regenerate the
  container. Otherwise, the service will just be restarted using the same files
  from the previous image.
* If you lost a bunch of disk space, you may use `docker system prune` to clean
  away old things. Note that you may also need to restart Docker, or wait for a
  reaper cron task to run, to compress the virtual disk image used by Docker.
  Pruning will not remove any explicitly tagged images, nor will it remove
  images that are depended on by explicitly tagged images.
* To look at a list of all containers or images on your host machine, including
  those not managed by `docker-compose`, run `docker container ls -a` or
  `docker image ls`. (Using `-a` with `docker image ls` will show intermediate
  layer images, which is not very helpful.) To look at all the layers of an
  image and each layer’s size, use `docker history <image-id>`.
* To find dependent images of another image, try this simple script:

  ```bash
  #!/usr/bin/env bash
  for i in $(docker images -q); do
    docker history $i | grep -q $1 && echo $i
  done | sort -u
  ```

* You do not need to regenerate the buildmaster image, or restart its service,
  when making changes to workers. Just restart the worker’s service.
* After making changes to workers’ `buildbot.cfg`, run
  `docker-compose restart buildbot`.
