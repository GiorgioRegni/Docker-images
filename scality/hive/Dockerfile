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

# Install hive
ENV HIVE_VERSION=2.1.1
ENV HIVE_SCHEMA_VERSION=2.1.0
ENV HIVE_URL=http://apache.cs.utah.edu/hive/
ENV HIVE_DIR=/opt/hive
RUN mkdir -p $HIVE_DIR
RUN curl -s "${HIVE_URL}/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz" | tar -xz -C $HIVE_DIR

# Add hive to path
ENV HIVE_HOME=$HIVE_DIR/apache-hive-${HIVE_VERSION}-bin
ENV PATH=$HIVE_HOME/bin:$PATH

# Set up for hive metastore
RUN $HADOOP_HOME/bin/hadoop fs -mkdir       /user
RUN $HADOOP_HOME/bin/hadoop fs -mkdir       /user/hive
RUN $HADOOP_HOME/bin/hadoop fs -mkdir       /user/hive/warehouse
RUN $HADOOP_HOME/bin/hadoop fs -chmod g+w   /tmp
RUN $HADOOP_HOME/bin/hadoop fs -chmod g+w   /user/hive/warehouse

# Remove extra log jar file to suppress warning (see https://issues.apache.org/jira/browse/HIVE-6162)
RUN rm $HIVE_HOME/lib/log4j-slf4j-impl-2.4.1.jar

# Install mysql
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y install mysql-server libmysql-java

# Add mysql jdbc jar to classpath
RUN ln -s /usr/share/java/mysql-connector-java.jar $HIVE_HOME/lib/mysql-connector-java.jar

# Set hive-site.xml with mysql info
ADD hive-site.xml.template $HIVE_HOME/conf/hive-site.xml

# Set up mysql
RUN service mysql start && \
    mysql -e'CREATE DATABASE metastore;' && \
    mysql -e'USE metastore;' && \
    mysql -e"CREATE USER 'hiveuser'@'localhost' IDENTIFIED BY 'hivepassword';" && \
    mysql -e"GRANT ALL PRIVILEGES ON *.* to 'hiveuser'@'localhost' identified by 'hivepassword';" && \
    mysql -e'flush privileges;'


# Set up schema
RUN service mysql start && $HIVE_HOME/bin/schematool -dbType mysql -initSchema

# Add mysql volume
VOLUME /var/lib/mysql

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Start mysql and hive metastore
WORKDIR $HIVE_HOME
ENTRYPOINT ["/entrypoint.sh"]
CMD service mysql start && bin/hive --service metastore
