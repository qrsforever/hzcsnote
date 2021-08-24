#!/bin/bash
cmd_check=`which kustomize`
if [[ x$cmd_check == x ]]
then
    curl -XGET https://github.91chifun.workers.dev/https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv4.2.0/kustomize_v4.2.0_linux_amd64.tar.gz -o /tmp/kustomize.tar.gz
    tar -xvf /tmp/kustomize.tar.gz -C /usr/bin
fi
kustomize version
