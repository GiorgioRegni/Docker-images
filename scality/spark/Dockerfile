# Inspired by https://hub.docker.com/r/singularities/spark/~/dockerfile/

FROM openjdk:8-jdk
MAINTAINER Lauren Spiegel <lauren.spiegel@scality.com>

# Update packages
RUN apt-get -qq -y update

# Software installation
RUN apt-get -qq -y install build-essential telnet iperf build-essential wget curl less rsync vim

# Install hadoop
ENV HADOOP_VERSION=2.7.2
ENV HADOOP_URL=http://www.us.apache.org/dist/hadoop/common/
ENV HADOOP_DIR=/opt/hadoop
# note that HADOOP_PREFIX is used when calling bin/hadoop commands so must be defined
ENV HADOOP_PREFIX=$HADOOP_DIR/hadoop-$HADOOP_VERSION
RUN mkdir -p $HADOOP_DIR
RUN curl -s "${HADOOP_URL}/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" | tar -xz -C $HADOOP_DIR

# Add AWS jar file to classpath
RUN sed -i '43i export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:/opt/hadoop/hadoop-2.7.2/share/hadoop/tools/lib/*' "${HADOOP_PREFIX}/etc/hadoop/hadoop-env.sh"

# Add s3 endpoint and accessKey/secretKey info
ADD core-site.xml.template $HADOOP_PREFIX/etc/hadoop/core-site.xml

# Add hadoop to path
ENV HADOOP_HOME=$HADOOP_PREFIX
ENV PATH=$HADOOP_HOME/bin:$PATH

# Install Spark
ENV SPARK_VERSION=2.1.0
ENV SPARK_HOME=/opt/spark/spark-$SPARK_VERSION

RUN mkdir -p "${SPARK_HOME}" \
  && export ARCHIVE=spark-$SPARK_VERSION-bin-without-hadoop.tgz \
  && export DOWNLOAD_PATH=apache/spark/spark-$SPARK_VERSION/$ARCHIVE \
  && curl -sSL https://mirrors.ocf.berkeley.edu/$DOWNLOAD_PATH | \
    tar -xz -C $SPARK_HOME --strip-components 1 \
  && rm -rf $ARCHIVE
COPY spark-env.sh $SPARK_HOME/conf/spark-env.sh
ENV PATH=$SPARK_HOME/bin:$PATH

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh

WORKDIR $SPARK_HOME

# Run script to update s3 configuration in hadoop with env variables sent to docker run command
ENTRYPOINT ["/entrypoint.sh"]
# Start spark shell
CMD bin/spark-shell
