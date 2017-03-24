#!/bin/bash

set -e

if [[ "$ACCESS_KEY" && "$SECRET_KEY" ]]; then
    sed -i "s/accessKey1/$ACCESS_KEY/" /opt/presto/etc/catalog/hive.properties
    sed -i "s/verySecretKey1/$SECRET_KEY/" /opt/presto/etc/catalog/hive.properties
    echo "Access key and secret key have been modified successfully"
fi

if [[ "$S3_ENDPOINT" ]]; then
    sed -i "s/http:\/\/127\.0\.0\.1:8000/$S3_ENDPOINT/" /opt/presto/etc/catalog/hive.properties
    echo "S3 Endpoint has been modified to $S3_ENDPOINT"
fi

exec "$@"
