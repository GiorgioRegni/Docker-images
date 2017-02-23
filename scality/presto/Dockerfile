FROM ubuntu:trusty
MAINTAINER Lauren Spiegel <lauren.spiegel@scality.com>

# Update packages.
RUN apt-get -qq -y update  

# Software installation
RUN apt-get -qq -y install build-essential telnet iperf build-essential wget curl 

# Install java
RUN apt-get install -y -q default-jdk

# what do when image starts
CMD bash
