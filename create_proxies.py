#!/usr/bin/env python

import sys
from os import environ
from os.path import join, exists
from base64 import b64decode


DOCKERFILE = """\
RlJPTSBrZXl3ZWV1c3Ivb25pb25iYXNlCgpFTlYgT1AgL2hvbWUvb25pb25wcm94eQpSVU4gdXNl
cmFkZCAtLWNyZWF0ZS1ob21lIC0tc2hlbGwgL2Jpbi9zaCBvbmlvbnByb3h5CkVOViBOR1ggL3Zh
ci9saWIvbmdpbngKV09SS0RJUiAkT1AKCiMgZml4IHRvbyBwZXJtaXNzaXZlIHBlcm1pc3Npb25z
IGJlZm9yZSBydW5uaW5nIHRoZSBzZXJ2aWNlClJVTiBta2RpciAkT1Avd3d3ICYmIGNob3duIC1S
IG9uaW9ucHJveHk6b25pb25wcm94eSAkT1Avd3d3ICYmIFwKICAgIGNobW9kIC1SIDA2NDQgJE9Q
L3d3dyAmJiBjaG1vZCAwNzAwICRPUC93d3cKCiMgY29uZmlndXJlIFRvciB0byBnZXQgLm9uaW9u
IGFkZHJlc3MsIGJ1dCB1c2UgZW1wdHkgZm9sZGVyClJVTiBlY2hvICJIaWRkZW5TZXJ2aWNlRGly
ICRPUC93d3ciID4+IC9ldGMvdG9yL3RvcnJjICYmIFwKICAgIGVjaG8gIkhpZGRlblNlcnZpY2VW
ZXJzaW9uIDIiID4+IC9ldGMvdG9yL3RvcnJjICYmIFwKICAgIGVjaG8gIkhpZGRlblNlcnZpY2VQ
b3J0IDgwIDEyNy4wLjAuMTo2NjY2IiA+PiAvZXRjL3Rvci90b3JyYwoKIyBzdGFydCBOR0lOWCBh
dCB0aGUgdXNlciBob21lIGxvY2F0aW9uIGluIGNvbnRhaW5lcgpVU0VSIG9uaW9ucHJveHkKRU5U
UllQT0lOVCBcCiAgICBuZ2lueCAtdCAtYyAkT1AvbmdpbnguY29uZiAmJiBcCiAgICBuZ2lueCAt
YyAkT1AvbmdpbnguY29uZiAtcCAkT1AgJiYgXAogICAgdG9yCgojIGNvcHkgY3VzdG9tIE5HSU5Y
IGNvbmZpZwpBUkcgbmdpbnhfY29uZgpDT1BZICRuZ2lueF9jb25mICRPUC9uZ2lueC5jb25mCgoj
IHJlcGxhY2UgcGxhY2Vob2xkZXIgd2l0aCB2YWx1ZSBmb3IgcHJveHlfcGFzcwpBUkcgU0VSVklD
RV9OQU1FClJVTiBzZWQgLWkgInN8T05JT05QUk9YWV9VUkx8JHtTRVJWSUNFX05BTUV9fGciICRP
UC9uZ2lueC5jb25mICYmIFwKICAgIGNhdCAkT1AvbmdpbnguY29uZgo=
"""
RAW_NAME = 'onionproxy'
VERSION = environ.get('VERSION', '1.0')
COMPOSE_NAME = 'docker-compose.yml'
IMAGE_NAME = f'keyweeusr/{RAW_NAME}'


def main(sources: list = None):
    if not sources:
        print('No list of sources found. Input proxy files!')
        exit(1)

    if not exists(join(environ['PWD'], 'proxies.txt')):
        print("The 'proxies.txt' was not found!")
        exit(1)

    with open(join(environ['PWD'], 'Dockerfile'), 'wb') as dfl:
        dfl.write(b64decode(DOCKERFILE.encode('utf-8')))

    with open(join(environ['PWD'], COMPOSE_NAME), 'w') as yml:
        yml.write("version: '3'\n")
        yml.write('services:\n')

    services = ''
    volumes = ''

    for file in sources:
        with open(join(environ['PWD'], file)) as source:
            source = source.readlines()

        for line in source:
            name, *url = line.split(';')
            url = ';'.join(url)
            conf = 'nginx-default.conf'

            services += f'    {name}:\n'
            services += f'        build:\n'
            services += f'            context: .\n'
            services += f'            dockerfile: Dockerfile\n'
            services += f'            args:\n'
            services += f'                nginx_conf: {conf}\n'
            services += f'                SERVICE_NAME: {url}\n'
            services += f'        image: {IMAGE_NAME}:{name}-{VERSION}\n'
            services += f'        volumes:\n'
            services += f'            - {name}:/home/{RAW_NAME}/www\n'
            services += f'        restart: always\n\n'
            volumes += f'    {name}:\n'

    with open(join(environ['PWD'], COMPOSE_NAME), 'a') as yml:
        yml.write(services)
        yml.write('volumes:\n')
        yml.write(volumes)


if __name__ == '__main__':
    main(sys.argv[1:])
