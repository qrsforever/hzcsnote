#!/bin/bash

if [[ x$(which kubectl) == x || x$(which kubelet) == x ]]
then
    RELEASE=v1.22.0 # "$(curl -sSL https://dl.k8s.io/release/stable.txt)"
    cd /usr/bin
    sudo curl -L --remote-name-all https://dl.k8s.io/${RELEASE}/bin/linux/amd64/{kubeadm,kubelet,kubectl}
    sudo chmod +x {kubeadm,kubelet,kubectl}
    sudo apt install bash-completion
    sudo kubectl completion bash > /etc/bash_completion.d/kubectl
fi
kubeadm version
kubelet version
kubectl version --client
