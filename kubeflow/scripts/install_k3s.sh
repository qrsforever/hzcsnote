#!/bin/bash
SRC_GPG=https://gitee.com/qrsforever/blog_source_assets/raw/master/Tutorial/k8s/apt-key.gpg
DST_GPG=/usr/share/keyrings/kubernetes-archive-keyring.gpg
sudo curl -XGET -L $SRC_GPG -o $DST_GPG
echo "deb [signed-by=$DST_GPG] http://mirrors.ustc.edu.cn/kubernetes/apt kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install -y kubeadm kubelet kubectl kubernetes-cni 
kubeadm version && kubelet --version && kubectl version
