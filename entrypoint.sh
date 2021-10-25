#!/bin/bash

TARGET_NOTE_DIR=/hzcsk12/hzcsnote

umask 0000; 

while true;
do
    jupyter notebook --no-browser --notebook-dir=$TARGET_NOTE_DIR --allow-root --ip=0.0.0.0 --port=8118
    sleep 3
done
