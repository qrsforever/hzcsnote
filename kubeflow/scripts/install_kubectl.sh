#!/bin/bash

cmd_check=`which kubectl`
if [[ x$cmd_check == x ]]
then
    RELEASE="$(curl -sSL https://dl.k8s.io/release/stable.txt)"
    cd {BIN_DIR}
    curl -L --remote-name-all https://dl.k8s.io/${RELEASE}/bin/linux/amd64/{kubeadm,kubelet,kubectl}
    apt install bash-completion
    kubectl completion bash > /etc/bash_completion.d/kubectl
fi
kubeadm version
kubelet version
kubectl version --client
