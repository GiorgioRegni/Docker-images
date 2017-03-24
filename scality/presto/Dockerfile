FROM openjdk:8-jdk
MAINTAINER Lauren Spiegel <lauren.spiegel@scality.com>

ENV PRESTO_VERSION=0.166
ENV PRESTO_URL https://repo1.maven.org/maven2/com/facebook/presto
ENV WORKDIR /opt/presto

# Update packages.
RUN apt-get -qq -y update

# Software installation
RUN apt-get -qq -y install build-essential telnet iperf build-essential wget curl less

# Install presto server
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

RUN curl "${PRESTO_URL}/presto-server/${PRESTO_VERSION}/presto-server-${PRESTO_VERSION}.tar.gz" | tar --strip-components=1 -xzv

# Install presto CLI
RUN curl "${PRESTO_URL}/presto-cli/${PRESTO_VERSION}/presto-cli-${PRESTO_VERSION}-executable.jar" -o ${WORKDIR}/bin/presto && chmod +x ${WORKDIR}/bin/presto

# Deploy configuration
ADD etc ${WORKDIR}/etc

VOLUME ["/data"]

# Smaller image footprint
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Run entrypoint script and start presto in foreground
ENTRYPOINT ["/entrypoint.sh"]
CMD [ "bin/launcher", "run" ]
