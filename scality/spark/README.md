# Spark Docker Image

This is a Spark Docker image intended to be used with Scality S3.

## Build the image

To build the image locally:

```
docker build -t scality/spark .
```
## Start a container

To run the container on Mac:

```
docker run -it --net=host --add-host=moby:127.0.0.1 -p 4040:4040 scality/spark
```

To run the container on Linux:

```
docker run -it --net=host --add-host=localhost.localdomain.localdomain:127.0.0.1 -p 4040:4040 scality/spark
```

To set an S3 accessKey/secreteKey pair other than accessKey1 and verySecretKey1,
add to docker run command:

```
-e ACCESS_KEY=newAccessKey -e SECRET_KEY=newSecretKey
```

To set an S3 endpoint other than http://127.0.0.1:8000, add to docker run command:

```
-e S3_ENDPOINT=newEndpoint
```

## Running Spark Shell

If you run the container, the spark shell will launch automatically using this command:

```
bin/spark-shell
```

If you would rather run spark in a different manner, you can alter the starting CMD.
