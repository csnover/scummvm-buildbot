FROM debian:9.2
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		certbot \
		cron && \
	rm -rf /var/lib/apt/cache/*
COPY crontab /etc/cron.d/certbot
CMD [ "cron", "-f" ]
