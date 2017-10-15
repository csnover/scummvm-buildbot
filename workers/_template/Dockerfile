# Please delete the template comments (including this one!) and any defaulted
# options when configuring your worker.

# When writing the Dockerfile, where possible, put operations most likely to
# change toward the end of the file. When an operation changes, it invalidates
# the caches of all successive operations as well.

# Choose the base image for use by the worker. Using the same default base image
# is best, if possible, since this data can then be shared by all workers.
ARG DEFAULT_BASE_IMAGE
FROM ${DEFAULT_BASE_IMAGE}

# Please provide some different contact information here if you are an
# individual maintainer for this worker.
LABEL maintainer="ScummVM Team <admin@scummvm.org>"

# The buildbot version will normally come from build-images.sh. This keeps all
# images using the same version of Buildbot.
ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}

# Create the unprivileged user and home directory which will be used by
# Buildbot. This home directory is where all of the working directories for each
# builder will be created (one subdirectory per builder), plus the startup
# script. Per convention, put the home directory at `/buildbot` instead of in
# its default place. Buildbot also needs a valid shell for executing shell
# commands on the worker.
RUN useradd -ms /bin/bash -d /buildbot buildbot

# If you want the worker to use the shared Git repository, the persistent data
# directory needs to be set up here and its permissions set appropriately so it
# can be written to by buildbot. Any other mount points for persistent data also
# need to be created here like this.
RUN mkdir -p /data/sharedrepo && chown buildbot:buildbot /data/sharedrepo

# All system packages should be installed here.
#
# The following system libraries/utilities are required for Buildbot:
#
# - dumb-init (retrievable from https://github.com/Yelp/dumb-init/releases if
#   needed)
# - git
# - openssl
# - pip (only if a compatible version of Buildbot is unavailable directly from
#   the package manager, or if installing from the package manager causes many
#   unnecessary dependencies to be installed)
# - python 2.6, 2.7, or 3.4+
#
# If possible, also install these dependencies from the OS's package manager
# instead of pip:
#
# - python-twisted
# - python-openssl (a.k.a. pyopenssl)
#
# If snapshot packaging is turned on, the following utilities are required:
#
# - gzip (if "tar.gz" archive format is used)
# - rsync
# - tar (if "tar", "tar.gz", or "tar.xz" archive format is used)
# - xz (if "tar.xz" archive format is used)
# - zip (if "zip" archive format is used)
#
# Use only ONE `RUN` command to install system packages! If the package manager
# has a mechanism to suppress caching of downloaded files, or a mechanism for
# suppression of non-essential dependencies, use them. Otherwise, make sure to
# at least manually delete the package manager's cache inside the *same*
# `RUN` command to avoid bloating the generated image. See the RUN section of
# Dockerfile Best Practices at
# <https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/>
# for more detailed information.
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		... && \
	rm -rf /var/lib/apt/lists/*

# If Buildbot is not available from the package manager, install it separately
# using pip.
RUN pip --no-cache-dir install \
		buildbot-worker==${BUILDBOT_VERSION}

# The rest of this is boilerplate that you should be able to leave alone. Only
# if dumb-init was not installed from the system's package manager, or you must
# use a non-standard buildbot user or directory, should you need to change any
# of this.
USER buildbot
WORKDIR /buildbot
COPY buildbot.tac /buildbot
CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
