#!/bin/bash
#=================================================================
# date: 2020-12-13 17:05:16
# title: run
# author: QRS
#=================================================================


cur_fil=${BASH_SOURCE[0]}
cur_dir=`cd $(dirname $cur_fil); pwd`
top_dir=`dirname $cur_dir`

PYTHONPATH=$top_dir:$PYTHONPATH python3 ./selenium/main.py
