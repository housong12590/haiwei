#!/usr/bin/env bash

git pull

docker rm -f haiwei

docker rmi -f haiwei

docker build -t haiwei .

docker run -d --name haiwei -p 8023:5000 haiwei
