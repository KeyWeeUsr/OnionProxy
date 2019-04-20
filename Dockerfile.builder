FROM python:3.7-alpine
ARG VERSION
ENV VERSION $VERSION

COPY create_proxies.py /opt/
WORKDIR /mnt
ENTRYPOINT python /opt/create_proxies.py proxies.txt
