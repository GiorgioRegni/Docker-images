#!/bin/bash 
#sec
DURATION=10 
CONNECTIONS=1
if [ ! -z "$1" ] ; then
	DURATION=$1
fi
if [ ! -z "$2" ] ; then
	CONNECTIONS=$2
fi  
docker rm -f victim  &> /dev/null 
docker rm -f agressor &> /dev/null 
docker run -d --name victim scality/netdebug  iperf -s  -t  $DURATION -y C &> /dev/null
IP=$(docker inspect victim | grep IPAddress | grep -o "172[^ \,\"]*"  | tail -n 1)
if [ ! -z "$3" ] ; then
	IP=$3
fi 
docker run -d --name agressor scality/netdebug iperf -c $IP  -t  $DURATION -P $CONNECTIONS  -d   -y C  &> /dev/null
TOP_DURATION=$((($DURATION*90)/100 )) 
echo "TOP REPORT"
top -b -n 2 -d $TOP_DURATION
#make sure the iperf tests have completed
SLEEP_DURATION=$((($DURATION*20)/100 ))  
sleep $SLEEP_DURATION
RUNNING=$(docker inspect agressor | grep -c running)
while [ $RUNNING -ne 0 ] ; do
	sleep 10 
	RUNNING=$(docker inspect agressor | grep -c running)
	echo "sleeping"
done   
echo "IPERF VICTIM"
docker logs --tail=all victim
echo "IPERF AGRESSOR"
docker logs --tail=all agressor
docker stop victim &> /dev/null
docker rm victim &> /dev/null
docker rm agressor &> /dev/null 
