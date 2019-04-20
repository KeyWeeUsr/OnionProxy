FROM keyweeusr/onionbase

ENV OP /home/onionproxy
RUN useradd --create-home --shell /bin/sh onionproxy
ENV NGX /var/lib/nginx
WORKDIR $OP

# fix too permissive permissions before running the service
RUN mkdir $OP/www && chown -R onionproxy:onionproxy $OP/www && \
    chmod -R 0644 $OP/www && chmod 0700 $OP/www

# configure Tor to get .onion address, but use empty folder
RUN echo "HiddenServiceDir $OP/www" >> /etc/tor/torrc && \
    echo "HiddenServiceVersion 2" >> /etc/tor/torrc && \
    echo "HiddenServicePort 80 127.0.0.1:6666" >> /etc/tor/torrc

# start NGINX at the user home location in container
USER onionproxy
ENTRYPOINT \
    nginx -t -c $OP/nginx.conf && \
    nginx -c $OP/nginx.conf -p $OP && \
    tor

# copy custom NGINX config
ARG nginx_conf
COPY $nginx_conf $OP/nginx.conf

# replace placeholder with value for proxy_pass
ARG SERVICE_NAME
RUN sed -i "s|ONIONPROXY_URL|${SERVICE_NAME}|g" $OP/nginx.conf && \
    cat $OP/nginx.conf
