ARG DEFAULT_32_BIT_BASE_IMAGE
FROM ${DEFAULT_32_BIT_BASE_IMAGE}
USER root

ARG URL=http://www.gcw-zero.com/files/opendingux-gcw0-toolchain.2014-08-20.tar.bz2
ARG SHASUM=c5ec0402fdbea95a537b1d8ad9cf905572cb7265319483dc54c3b1e1daee2a08cadb84aa81d88c41dcfaa04423706e48

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		bzip2 \
		ca-certificates \
		wget && \
	rm -rf /var/lib/apt/lists/* && \
	wget --progress=bar:force:noscroll -O gcw0.tar.bz2 ${URL} && \
	echo "$SHASUM *gcw0.tar.bz2" | sha384sum -c && \
	tar xjf gcw0.tar.bz2 && \
	rm gcw0.tar.bz2

ENV PATH=/opt/gcw0-toolchain/usr/bin:$PATH

USER buildbot
WORKDIR /buildbot
