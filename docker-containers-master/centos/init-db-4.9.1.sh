#!/bin/sh

mkdir -p $1/mysql
mkdir -p $1/runtime

docker run -i -t -h powa -dns 127.0.0.1 \
    -v $1:/tmp/shared \
    brazil:5000/powa/4.9.1 cp -rp /var/lib/mysql /tmp/shared/
