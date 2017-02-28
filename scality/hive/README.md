# Hive Docker Image

This is a single instance Hive Docker image.

## Build the image

To build the image locally:

```
docker -t build scality/hive .
```
## Start a container

To run the container:

```
docker run --net=host --add-host=moby:127.0.0.1 scality/hive
```

To run the container on Linux:

```
docker run --net=host --add-host=localhost.localdomain.localdomain:127.0.0.1 scality/hive
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

## Running Beeline

Exec into the running container:

```
docker exec -it <container-id> bash
```

Start hiveserver2:

```
bin/hiveserver2 &
```

Start Beeline:

```
bin/beeline -u jdbc:hive2://localhost:10000
```

## Running Hive CLI (Note: Deprecated)

Exec into the running container:

```
docker exec -it <container-id> bash
```

Start the CLI:

```
bin/hive
```
