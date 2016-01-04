FROM java:8-jre
MAINTAINER Giorgio Regni @GiorgioRegni

# Set default Logstash version
ENV LOGSTASH_VERSION 1.4.5

# Set default Logstash source directory
ENV LOGSTASH_SRC_DIR /opt/logstash

# Set default data directory
ENV DATA_DIR /data

RUN apt-get update
RUN apt-get install wget curl netcat -y

# Download and install the Public Signing Key:
RUN wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch |  apt-key add -

# Add the repository definition to your /etc/apt/sources.list file:
RUN echo "deb http://packages.elastic.co/logstash/2.1/debian stable main" >> /etc/apt/sources.list
RUN echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" >> /etc/apt/sources.list

RUN apt-get update
#RUN apt-get install openjdk-8-jre-headless -y


# Download and install Logstash
RUN apt-get install logstash -y --force-yes

# Download and install elasticsearch
RUN apt-get install elasticsearch -y --force-yes

# Copy build files to container root
RUN mkdir /app
ADD . /app

# Set the working directory
WORKDIR ${LOGSTASH_SRC_DIR}

# Install Kibana
RUN curl -fSL https://download.elastic.co/kibana/kibana/kibana-4.3.1-linux-x64.tar.gz -o kibana.tar.gz
RUN mkdir kibana
RUN tar -xz --strip-components=1 -C kibana -f kibana.tar.gz
RUN rm kibana.tar.gz

# Define mountable directory
VOLUME ${DATA_DIR}


ENV PATH ${LOGSTASH_SRC_DIR}/kibana/bin:${LOGSTASH_SRC_DIR}/bin:$PATH

# Kibana
EXPOSE 5601

# Elastic Search
EXPOSE 9200

CMD ["bash", "/app/bin/run"]
