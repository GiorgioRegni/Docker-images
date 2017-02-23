FROM ubuntu:trusty
MAINTAINER Lauren Spiegel <lauren.spiegel@scality.com>

ENV PRESTO_VERSION=0.166
ENV PRESTO_URL https://repo1.maven.org/maven2/com/facebook/presto/
ENV WORKDIR /opt/presto

# Update packages.
RUN apt-get -qq -y update  

# Software installation
RUN apt-get -qq -y install build-essential telnet iperf build-essential wget curl 

# Install java
RUN apt-get install -y -q default-jdk

# Install presto
RUN mkdir -p /opt/presto
WORKDIR ${WORKDIR}

RUN curl "${BASE_URL}/presto-server/${PRESTO_VERSION}/presto-server-${PRESTO_VERSION}.tar.gz" | tar --strip-components=1 -xzv

VOLUME ["/data"]

# Start presto in foreground
CMD [ "bin/launcher", "run" ]
