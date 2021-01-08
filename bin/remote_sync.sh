#!/bin/bash

# /etc/hosts
# 116.85.66.182 gamma101
# 116.85.52.232 gamma102
# 116.85.45.189 gamma103
# 116.85.10.61  gamma104
# 116.85.24.143 gamma105

HOSTS=(
    "lidong@116.85.54.39"
    "lidong@116.85.66.182"
    "lidong@116.85.52.232"
    "lidong@116.85.45.189"
    "lidong@116.85.10.61"
    "lidong@116.85.24.143"
)

SRC_ROOT='/home/lidong/workspace/codes/hzcsai_com/hzcsk12'

__reboot_system() {
    ssh $1 "sudo reboot"
}

__update_codes() {
    ssh $1 "cd $SRC_ROOT; git pull"
}

__restart_services() {
    ssh $1 "cd $SRC_ROOT; sudo ./scripts/k12ai.sh all restart"
}

__run_command() {
    ssh $1 "$2"
}

__main() {
    echo "Select:"
    echo "0. reboot system"
    echo "1. update codes"
    echo "2. restart services"
    echo "3. run command"
    echo -n "Input:"
    read select

    if [[ x$select == x3 ]]
    then
        echo -n "Command > "
        read cmd
    fi
    for host in ${HOSTS[@]}
    do
        echo "sync: $host"
        case $select in
            1)
                __update_codes $host
                ;;
            2)
                __restart_services $host
                ;;
            3)
                __run_command $host "$cmd"
                ;;
            0)
                __reboot_system $host
                ;;
        esac
    done
}

__main
