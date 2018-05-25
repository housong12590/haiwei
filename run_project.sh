#!/usr/bin/env bash

PROJECT_NAME=haiwei1

docker rm -f ${PROJECT_NAME}
docker rmi -f ${PROJECT_NAME}
docker build -t ${PROJECT_NAME} .
docker run -d --name ${PROJECT_NAME} -p 8024:5000 ${PROJECT_NAME}



