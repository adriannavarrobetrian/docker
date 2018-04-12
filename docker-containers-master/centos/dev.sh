#!/bin/sh

# ./dev.sh <instance> <powa directory> <webapps directory> <your username> <command>

# <instance> = shared folder for mysql and template runtime
# <powa directory> = powa project directory. JRebels needs to reload changes.
# <webapps directory> = exploded powa webapps directory.
# <command> = bash             => opens a bash
#           = /opt/powa/run.sh => runs powa

# example
# ./dev.sh /opt/powa/instance /home/fabio/powa /opt/powa/webapps /opt/powa/run.sh

mkdir -p $1/mysql
mkdir -p $1/runtime

if [ ! -z $5 ]
then
  docker run -i -t -h powa -dns 127.0.0.1 \
    -p 80:80 \
    -p 443:443 \
    -p 3306:3306 \
    -p 8085:8085 \
    -p 61616:61616 \
    -v $1/mysql:/var/lib/mysql \
    -v $1/runtime:/powa/template/WebContent/WEB-INF/template/runtime \
    -v $2:/powa \
    -v $3:/opt/tomcat/webapps \
    sulley:5000/powaweb/dev $4
else
  docker run -i -t -h powa -dns 127.0.0.1 \
    -p 80:80 \
    -p 443:443 \
    -p 3306:3306 \
    -p 8085:8085 \
    -p 61616:61616 \
    -v $1/mysql:/var/lib/mysql \
    -v $1/runtime:/powa/template/WebContent/WEB-INF/template/runtime \
    -v $2:/powa \
    -v $3:/opt/tomcat/webapps \
    sulley:5000/powaweb/dev $4
fi
