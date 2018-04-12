FROM centos

RUN yum -y update
RUN yum -y install mysql mysql-server httpd dnsmasq unzip install openssh-clients rsync mod_ssl

# JAVA
RUN wget -O /tmp/java.tar.gz --no-check-certificate --no-cookies --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com" "http://download.oracle.com/otn-pub/java/jdk/7u40-b43/jdk-7u40-linux-x64.tar.gz"
RUN cd /opt && tar xzf /tmp/java.tar.gz && mv /opt/jdk1.7.0_40 /opt/java

RUN echo "export JAVA_HOME=/opt/java" >> /etc/profile.d/java.sh && echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> /etc/profile.d/java.sh

# TOMCAT
RUN wget -O /tmp/tomcat.tar.gz http://mirror.catn.com/pub/apache/tomcat/tomcat-7/v7.0.42/bin/apache-tomcat-7.0.42.tar.gz
RUN cd /opt && tar xzf /tmp/tomcat.tar.gz && mv /opt/apache-tomcat-7.0.42 /opt/tomcat

RUN echo "export TOMCAT_HOME=/opt/tomcat" >> /etc/profile.d/java.sh

# ACTIVEMQ
RUN wget -O /tmp/activemq.tar.gz http://mirror.catn.com/pub/apache/activemq/apache-activemq/5.8.0/apache-activemq-5.8.0-bin.tar.gz
RUN cd /opt && tar xzf /tmp/activemq.tar.gz && mv /opt/apache-activemq-5.8.0 /opt/activemq

RUN echo "export ACTIVEMQ_HOME=/opt/activemq" >> /etc/profile.d/java.sh

# JCE
RUN wget -O /tmp/jce.zip --no-check-certificate --no-cookies --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com" "http://download.oracle.com/otn-pub/java/jce/7/UnlimitedJCEPolicyJDK7.zip"
RUN cd /tmp/ && unzip /tmp/jce.zip && cp /tmp/UnlimitedJCEPolicy/*.jar /opt/java/jre/lib/security/

# MYSQL init script error if not found
RUN touch /etc/sysconfig/network
# secure mysql calling:
# /usr/bin/mysql_secure_installation

# dnsmasq
RUN printf 'address="/dbhost/127.0.0.1"\naddress="/jmshost/127.0.0.1"\naddress="/smtphost/127.0.0.1"' >> /etc/dnsmasq.d/0powa
RUN printf 'listen-address=127.0.0.1\nresolv-file=/etc/resolv.dnsmasq.conf\nconf-dir=/etc/dnsmasq.d\nuser=root' >> /etc/dnsmasq.conf
RUN printf 'nameserver 8.8.8.8\nnameserver 8.8.4.4' >> /etc/resolv.dnsmasq.conf

# cleaning
RUN rm -rf /tmp/* && yum -y clean headers packages

RUN mkdir -p /opt/powa/ && printf "#!/bin/bash\nsource /etc/bashrc\nservice dnsmasq start\nservice postfix start\nservice httpd start\nservice mysqld start\ncd /opt/activemq/bin\n./activemq start\ncd /opt/tomcat/bin/\n./powa.sh" > /opt/powa/run.sh
RUN chmod +x /opt/powa/run.sh

# manual steps
# configure mysql root password
# copy httpd conf directory
# install mod_jk
# update tocopy folder, powa.sh and secret
# install global collect certs
# install sshd to remote access
# install jrebel
# powa webapps, web folder
