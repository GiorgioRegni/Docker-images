
FROM scality/ironman-base:latest
MAINTAINER Marc "marc.segura@scality.com"

#------------------------------------
# ENVIRONMENT
#------------------------------------
ENV HOME=/home/ironman
ENV APT_SCALITY_LOGIN=marc.segura
ENV APT_SCALITY_PASSWORD=92Bastide
# Leave empty to take the default provided by the scality repo
ENV MINOR_VERSION=513
ENV CODE_NAME=lorien

#------------------------------------
# INSTALL SPROXYD
#------------------------------------
# this should go in the base image
USER root
RUN apt-get install -y -q libfcgi0ldbl libfcgi-dev
RUN echo "deb [arch=amd64] http://${APT_SCALITY_LOGIN}:${APT_SCALITY_PASSWORD}@packages.scality.com/stable_${CODE_NAME}_${MINOR_VERSION}/ubuntu/ trusty main" > /etc/apt/sources.list.d/scality.list
RUN echo "deb http://us.archive.ubuntu.com/ubuntu trusty main multiverse" >> /etc/apt/sources.list
RUN gpg --keyserver pgp.mit.edu --recv-keys 4A23AD0E && gpg -a --export 4A23AD0E | sudo apt-key add -
RUN apt-get update -q && apt-get install --ignore-missing  --no-install-recommends  -y -q scality-sproxyd scality-sagentd scality-sproxyd-apache2 
COPY ./deployment/sproxyd.conf /etc/sproxyd.conf
# create the directories apache needs to run
RUN bash   -c "source /etc/apache2/envvars  && export && mkdir -p \${APACHE_LOCK_DIR} && mkdir -p \${APACHE_LOG_DIR} && mkdir -p  \${APACHE_RUN_DIR}" 
USER ironman

#------------------------------
# CONFIGURE SUPERVISOR
#------------------------------
# see http://supervisord.org/configuration.html
RUN mkdir ${HOME}/log
VOLUME [ "${HOME}/${PROJECT}/log"]
COPY ./deployment/supervisord.conf ${HOME}/supervisord.conf

#---------------------------
# CIRCLECI CHANGES
#---------------------------
USER root
RUN apt-get remove -y -q  docker-engine
RUN wget https://apt.dockerproject.org/repo/pool/main/d/docker-engine/docker-engine_1.6.2-0~trusty_amd64.deb
RUN export DEBIAN_FRONTEND=noninteractive && export DEBIAN_PRIORITY=critical&&  dpkg -i docker-engine_1.6.2-0~trusty_amd64.deb
RUN chmod a+x  /root/hosts.bash
USER ironman

CMD while [ ! -e /var/run/docker.sock ] ; do sleep 1 ; done && sudo /usr/bin/supervisord -c ${HOME}/supervisord.conf &&  tail -f ${HOME}/log/*
