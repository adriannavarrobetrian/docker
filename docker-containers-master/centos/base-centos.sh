#/bin/sh

# use to create another test image

# rebuild database
# rsync webapps
#     ex: rsync -ravzp --delete fabio@10.10.100.221:/opt/tomcat/webapps/ /opt/tomcat/webapps/

# (these instructions need to be commited on base-centos instead)
# add spirit api properties to engine.deploy.properties 
# remove any tmp tomcat file
# disable jrebel, debug, jmx on powa.sh

docker run -i -t -h powa -dns 127.0.0.1 \
    -p 80:80 \
    -p 443:443 \
    -p 3306:3306 \
    brazil:5000/powa/base-centos bash
