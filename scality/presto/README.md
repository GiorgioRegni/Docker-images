# Presto Docker Image

This is a single instance Presto Docker image with the worker and coordinator on the same machine.
It is configured to use a Hive connector.

## Build the image

To build the image locally:

```
docker -t build scality/presto .
```
## Start a container

To run the container on Mac:

```
docker run --net=host --add-host=moby:127.0.0.1 scality/presto
```

To run the container on Linux:

```
docker run --net=host --add-host=localhost.localdomain.localdomain:127.0.0.1 scality/presto
```

## Running Presto

Exec into the running container:

```
docker exec -it <container-id> bash
```

Start the CLI:

```
cd /opt/presto/bin
./presto --catalog hive --schema default
```
