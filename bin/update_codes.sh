#!/bin/bash

# /etc/hosts
# 116.85.66.182 gamma101
# 116.85.52.232 gamma102
# 116.85.45.189 gamma103
# 116.85.10.61  gamma104
# 116.85.24.143 gamma105

hosts=("gamma101" "gamma102" "gamma103" "gamma104" "gamma105")

for hostname in ${hosts[@]}
do
    echo "sync codes: $hostname"
    ssh lidong@$hostname "cd /home/lidong/workspace/codes/hzcsai_com/hzcsk12; git pull"
done
