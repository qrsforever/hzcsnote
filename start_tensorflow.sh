#!/bin/bash

CUR_DIR=$(cd $(dirname ${BASH_SOURCE[0]}); pwd)

docker run -it -u $(id -u):$(id -g) --runtime nvidia --name tf-note -p 8888:8888 \
    -v $CUR_DIR/tensorflow:/tf/tensorflow \
    -v /data:/data \
    -v /raceai:/raceai \
    tensorflow/tensorflow:latest-gpu-jupyter
