#!/bin/sh

# ./run.sh <data directory> <command>

# <instance> = shared folder for mysql and template runtime
# <command> = bash             => opens a bash
#           = /opt/powa/run.sh => runs powa

mkdir -p $1/mysql
mkdir -p $1/runtime

# example
# ./run.sh /opt/powa/release /opt/powa/run.sh
docker run -i -t -h powa -dns 127.0.0.1 \
    -p 80:80 \
    -p 443:443 \
    -p 3306:3306 \
    -v $1/mysql:/var/lib/mysql \
    -v $1/runtime:/opt/tomcat/webapps/template/WEB-INF/template/runtime \
    brazil:5000/powa/4.9.1 $2
