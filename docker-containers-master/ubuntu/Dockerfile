FROM ubuntu

RUN apt-get update
RUN apt-get -y install wget

# JAVA
RUN wget -O /opt/java.tar.gz --no-check-certificate --no-cookies --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com" "http://download.oracle.com/otn-pub/java/jdk/7u40-b43/jdk-7u40-linux-x64.tar.gz"
RUN cd /opt && tar xzf java.tar.gz
RUN ln -s /opt/jdk1.7.0_40 /opt/java

RUN echo "export JAVA_HOME=/opt/java" >> /etc/profile.d/java.sh
RUN echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> /etc/profile.d/java.sh

RUN rm /opt/java.tar.gz

# TOMCAT
RUN wget -O /opt/tomcat.tar.gz http://mirror.catn.com/pub/apache/tomcat/tomcat-7/v7.0.42/bin/apache-tomcat-7.0.42.tar.gz
RUN cd /opt && tar xzf tomcat.tar.gz
RUN ln -s /opt/apache-tomcat-7.0.42 /opt/tomcat

RUN echo "export TOMCAT_HOME=/opt/tomcat" >> /etc/profile.d/java.sh

RUN rm -rf /opt/tomcat/webapps
RUN rm /opt/tomcat.tar.gz

# ACTIVEMQ
RUN wget -O /opt/activemq.tar.gz http://mirror.catn.com/pub/apache/activemq/apache-activemq/5.8.0/apache-activemq-5.8.0-bin.tar.gz
RUN cd /opt && tar xzf activemq.tar.gz
RUN ln -s /opt/apache-activemq-5.8.0 /opt/activemq

RUN echo "export ACTIVEMQ_HOME=/opt/activemq" >> /etc/profile.d/java.sh

RUN rm /opt/activemq.tar.gz

# JCE
RUN apt-get -y install unzip
RUN wget -O /opt/jce.zip --no-check-certificate --no-cookies --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com" "http://download.oracle.com/otn-pub/java/jce/7/UnlimitedJCEPolicyJDK7.zip"
RUN cd /opt/ && unzip jce.zip
RUN cp /opt/UnlimitedJCEPolicy/*.jar /opt/java/jre/lib/security/
RUN rm /opt/jce.zip
RUN rm -rf /opt/UnlimitedJCEPolicy

# MYSQL
RUN debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password #hermesdb'
RUN debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password #hermesdb'
RUN apt-get -y install mysql-server

# APACHE
RUN apt-get -y install apache2

# secure mysql calling:
# /usr/bin/mysql_secure_installation

# dnsmasq
RUN apt-get -y install dnsmasq
RUN echo 'address="/dbhost/127.0.0.1"' >> /etc/dnsmasq.d/0powa
RUN echo 'address="/jmshost/127.0.0.1"' >> /etc/dnsmasq.d/0powa
RUN echo 'address="/smtphost/127.0.0.1"' >> /etc/dnsmasq.d/0powa
RUN echo 'listen-address=127.0.0.1' >> /etc/dnsmasq.conf
RUN echo 'resolv-file=/etc/resolv.dnsmasq.conf' >> /etc/dnsmasq.conf
RUN echo 'conf-dir=/etc/dnsmasq.d' >> /etc/dnsmasq.conf
RUN echo 'nameserver 8.8.8.8' >> /etc/resolv.dnsmasq.conf
RUN echo 'nameserver 8.8.4.4' >> /etc/resolv.dnsmasq.conf

RUN apt-get clean
