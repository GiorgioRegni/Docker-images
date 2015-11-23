FROM centos:centos7
MAINTAINER Chris Cuming ccuming@gmail.com
# hello
# Update packages.
RUN yum update -y

# Install curl and git
RUN yum install -y curl git

# EPEL setup.
RUN rpm --import http://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-7
RUN yum install -y epel-release

# Install zeromq.
RUN yum install -y zeromq

# Create the "ironman" user.
RUN useradd -ms /bin/bash ironman

# Run as the "ironman" user.
USER ironman

# TODO: NVM and Node install for ironman user.
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.26.1/install.sh | bash
RUN source ~/.bash_profile && nvm install v4.1.2 && nvm alias default v4.1.2
