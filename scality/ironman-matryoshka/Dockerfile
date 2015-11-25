FROM scality/ironman-base:dev_FT_Base
MAINTAINER Marc  "marc.segura@scality.com"

#############################################
# all the stuff required to access github
# the branch we want to extract data from
ENV BRANCH=dev/FT/Base
# repo owner
ENV OWNER=GiorgioRegni
ENV REPO=Docker-images
#############################################

USER root

#-----------------------------------------
# INSTALL matryoshka
#----------------------------------------
RUN  mkdir matryoshka
RUN  curl -O -L https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/scality/ironman-matryoshka/deployment/matryoshka/setup.py
RUN  cd matryoshka && curl -O -L https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/scality/ironman-matryoshka/deployment/matryoshka/matryoshka/matryoshka.py
RUN  python setup.py install

#------------------------------
# CONFIGURE SUPERVISOR
#------------------------------
# see http://supervisord.org/configuration.html
RUN mkdir ${HOME}/log
RUN cd /root && curl -O -L https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/scality/ironman-matryoshka/deployment/supervisord.conf

#-------------------------
# TEST SUITE MAPPING
#-------------------------
RUN mkdir /test
VOLUME /test

#---------------------------------------------------
# WHAT TO DO WHEN THE INSTANCE STARTS
#--------------------------------------------------
CMD /usr/bin/supervisord -c /root/supervisord.conf &&  /usr/local/bin/matryoshka.py ${IMAGE} /test

