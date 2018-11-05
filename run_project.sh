#!/usr/bin/env bash

PROJECT_NAME=tx_ops

docker rm -f ${PROJECT_NAME}
docker rmi -f ${PROJECT_NAME}
docker build -t ${PROJECT_NAME} .
docker run -d --name ${PROJECT_NAME} \
    -e DEBUG=true \
    -e MYSQL_HOST='123.207.152.86' \
    -e MYSQL_USER='root' \
    -e MYSQL_PASSWORD='123546' \
    -e MYSQL_DB='ghost' \
    -p 8023:5000 ${PROJECT_NAME}



