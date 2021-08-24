#!/bin/bash

cmd_check=`which kfctl`
if [[ x$cmd_check == x ]]
then
    curl -X GET https://github.91chifun.workers.dev/https://github.com//kubeflow/kfctl/releases/download/v1.2.0/kfctl_v1.2.0-0-gbc038f9_linux.tar.gz -o /tmp/kfctl.tar.gz
    sudo tar -xvf /tmp/kfctl.tar.gz -C /usr/bin
fi
kfctl version
