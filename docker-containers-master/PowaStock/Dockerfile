#PowaStock μ-service
#
# VERSION 1

FROM dockerfile/ubuntu

MAINTAINER marcosbernal@powa.com 

#Install Java
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN apt-get install -y oracle-java7-installer

# Stockservice jar
ADD ./powa-stock-service-0.1.0-SNAPSHOT-standalone.jar /root/stock-service.jar

ENV STOCK_DB_SUBPROTOCOL "mysql"
ENV STOCK_DB_SUBNAME "//localhost:3306/stock" 
ENV STOCK_DB_USER "root"
ENV STOCK_DB_PASSWORD "#hermesdb"

# Default entrypoint
CMD ["java","-jar", "stock-service.jar"]
EXPOSE 3000
