FROM ubuntu:trusty
MAINTAINER Lauren Spiegel <lauren.spiegel@scality.com>

# Update packages.
RUN apt-get -qq -y update  

# Software installation
RUN apt-get -qq -y install build-essential telnet iperf build-essential wget curl 

# Install java
RUN apt-get install -y -q default-jdk

# Install presto
RUN mkdir -p /opt/presto
WORKDIR /opt/presto

RUN curl "https://repo1.maven.org/maven2/com/facebook/presto/presto-server/0.166/presto-server-0.166.tar.gz" -o /opt/presto/presto.tar.gz

RUN tar --strip-components=1 -xzf /opt/presto/presto.tar.gz

VOLUME ["/data"]

# what do when image starts
CMD bash
