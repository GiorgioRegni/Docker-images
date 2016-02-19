#!/bin/bash

#-----------------------------------------
# SCRIPT TO STARTUP THE DOCKER INSTANCE
#----------------------------------------

# Don't do anything until the docker socket
# is available (we can not populate the /etc/hosts
# otherwise)
while [ ! -e /var/run/docker.sock ] ; do
  sleep 1 ;
done

# when supervisord ends, the docker instance ends
sudo /usr/bin/supervisord -c ${HOME}/supervisord.conf && sleep 30s &&  tail -f ${HOME}/log/*
