#!/usr/bin/env bash

PROJECT_NAME=kx_ops

docker rm -f ${PROJECT_NAME}
docker rmi -f ${PROJECT_NAME}
docker build -t ${PROJECT_NAME} .
docker run -d --name ${PROJECT_NAME} \
    -e DEBUG=true \
    -e MYSQL_HOST='192.168.0.210' \
    -e MYSQL_USER='root' \
    -e MYSQL_PASSWORD='hJYC8PsOsUR45wnDQtGle8cqCFbmN9eY' \
    -e MYSQL_DB='kx_ops' \
    -p 8023:5000 ${PROJECT_NAME}



