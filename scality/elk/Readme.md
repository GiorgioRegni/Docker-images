# This is a self contained ELK stack in one container

Run with
   docker run -d -p 5601:5601  -p 9200:9200  scality/elk
   

This will pull the image automatically, elasticsearch will be listening on port 9200 and the kibana web UI on 5601.
It takes around a minute for the entire stack to run, be aware.
