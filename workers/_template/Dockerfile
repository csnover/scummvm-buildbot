# Please delete the template comments (including this one!) and any defaulted
# options when configuring your worker.

# When writing the Dockerfile, where possible, put operations most likely to
# change toward the end of the file, followed by inexpensive operations. When an
# operation changes, it invalidates the caches of all successive operations as
# well, so reducing the number and complexity of invalidated operations is
# important when rebuilding images.

# Choose the base image for use by the worker. Using the same default base image
# is best, if possible, since this data can then be shared by all workers. If
# you are starting from a source Docker image that uses a different base, you
# can copy out of the source image using `COPY --from` to keep a common base;
# see <https://docs.docker.com/engine/userguide/eng-image/multistage-build/> for
# details.
ARG DEFAULT_BASE_IMAGE
FROM ${DEFAULT_BASE_IMAGE}

# The default build context on the host is the `workers` directory, so that you
# can access common files by referencing them as `common`. When copying
# worker-specific files, reference the worker's directory by using $WORKER_NAME
# instead of hard-coding the worker's name in the COPY operations.
# Note that if you use $WORKER_NAME after more than one FROM operation, you will
# need to duplicate this ARG after each FROM.
ARG WORKER_NAME

# Please provide some different contact information here if you are an
# individual maintainer for this worker.
LABEL maintainer="ScummVM Team <admin@scummvm.org>"

# The buildbot version will normally come from build-images.sh. This keeps all
# images using the same version of Buildbot. If you use the default base image,
# you do not need to install Buildbot yourself and can delete this.
ARG BUILDBOT_VERSION
LABEL buildbot-version=${BUILDBOT_VERSION}

# All system packages should be installed here. If you use the default base
# image, you do not need to install any of these packages yourself and can
# delete this section.
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
		ccache \
		dumb-init \
		git \
		gzip \
		make \
		python-openssl \
		python-pip \
		python-twisted \
		rsync \
		xz-utils \
		... && \
	rm -rf /var/lib/apt/lists/*

# If Buildbot is not available from the package manager, install it separately
# using pip. If you use the default base image, you do not need to install
# Buildbot yourself and can delete this.
RUN pip --no-cache-dir install \
		buildbot-worker==${BUILDBOT_VERSION}

# For cross-compilers that don't install to a standard system directory like
# /usr/local/bin, specify the path to the compiler's executables here. It is
# also possible to set this in the Buildbot builder configuration if the worker
# has multiple conflicting paths that require only one path to be used at a
# time.
ENV PATH=/path/to/cross-compiler/bin:$PATH

# If you want the worker to use any writable shared or persistent data
# directories, create them here, setting permissions appropriately so they can
# be written to by the buildbot user. The default base image creates writable
# /data/ccache and /data/sharedrepo mount points, so you can delete this if you
# are using the default base image and are satisfied with the defaults.
RUN mkdir -p /data/shared && \
	chown buildbot:buildbot /data/shared

# Always make sure to switch back to the buildbot user & working directly at the
# end of the Dockerfile, or Buildbot will not function.
USER buildbot
WORKDIR /buildbot

# The rest of this is boilerplate that you should be able to use as-is, or just
# delete if you are using the default base image. You should only need to change
# any of this if dumb-init was not installed from the system's package manager,
# or you must use a non-standard buildbot user or directory (this is unlikely).
COPY common/buildbot.tac /buildbot
CMD ["/usr/bin/dumb-init", "twistd", "-ny", "buildbot.tac"]
