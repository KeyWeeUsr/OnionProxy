#!/bin/sh
set -e

VERSION=1.0


print_hostnames() {
    for serv in $(docker-compose ps| awk 'NR>2{print $1}')
    do
        $(which echo) -e "$serv\t$(docker exec -it $serv cat www/hostname)"
    done
}


recreate_compose() {
    docker build \
        --tag keyweeusr/onionproxy:builder-${VERSION} \
        --file Dockerfile.builder \
        --build-arg VERSION=${VERSION} \
        "$(pwd)"

    docker run \
        --interactive --tty \
        --volume $(pwd):/mnt \
        keyweeusr/onionproxy:builder-${VERSION}
}


deploy_proxies() {
    docker-compose up -d --build --force-recreate
}


if [ "$1" = "--hostnames" ]
then
    print_hostnames
    exit 0
fi

if [ ! -f "docker-compose.yml" ] || [ "$1" = "--recreate" ]
then
    recreate_compose
fi

deploy_proxies
print_hostnames
