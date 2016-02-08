# This is a self contained ELK stack in one container

Run with
  docker run -d -p 514:514 -p 514:514/udp -p 5601:5601  -p 9200:9200  scality/elk 

This will pull the image automatically, elasticsearch will be listening on port 9200 and the kibana web UI on 5601.
Syslog server is running on both udp and tcp port 514

It takes around a minute for the entire stack to run, be aware.
