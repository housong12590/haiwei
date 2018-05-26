#!/usr/bin/env bash

PROJECT_NAME=tx_ops

docker rm -f ${PROJECT_NAME}
docker rmi -f ${PROJECT_NAME}
docker build -t ${PROJECT_NAME} .
docker run -d --name ${PROJECT_NAME} -p 8023:5000 ${PROJECT_NAME}



