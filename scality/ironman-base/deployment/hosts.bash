#!/bin/bash
# fix the hostnames
for name in $(docker ps --format "{{.Names}}") ; do echo $name ; docker exec -u root $name /sbin/sysctl -w kernel.hostname=$name ; done
# fix /etc/hosts
tempfile=/tmp/hosts$RANDOM
for cid in $(docker ps -q) ; do 
    	name=$(docker inspect ${cid} | grep Name | head -n 1 |  cut -d\/ -f 2 | cut -d\" -f 1);
    	ip=$(docker inspect ${cid} | grep -v \"\" | grep \"IPAddress\" | cut -d\" -f 4 | head -n 1)
    	ipv6=$(docker inspect ${cid}| grep -v \"\" | grep \"GlobalIPv6Address\" | cut -d\" -f 4 | head -n 1)
    	if [ ! -z "${ip}" ]; then
        	echo ${ip} ${name} >>  ${tempfile}
    	else
       		if [ ! -z "${ipv6}" ]; then
       			echo ${ipv6} ${name} >>  ${tempfile}
       		fi 
    	fi
done 
echo "127.0.0.1 localhost" >> ${tempfile}
cp ${tempfile}  /etc/hosts
rm ${tempfile}
