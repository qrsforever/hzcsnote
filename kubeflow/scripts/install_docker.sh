
#!/bin/bash

cmd_check=`which docker`
if [[ x$cmd_check == x ]]
then
    sudo apt-get update
    sudo apt-get install apt-transport-https ca-certificates curl software-properties-common -y

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    sudo add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable"

    sudo apt-get update
    sudo apt-get install docker-ce -y

    cat > /etc/docker/daemon.json << EOF
    {
        "exec-opts": ["native.cgroupdriver=systemd"],
        "log-driver": "json-file",
        "log-opts": {
            "max-size": "100m"
        },
        "storage-driver": "overlay2",
        "runtimes": {
            "nvidia": {
                "path": "nvidia-container-runtime",
                "runtimeArgs": []
            }
        },
        "registry-mirrors": ["https://b9pmyelo.mirror.aliyuncs.com"]
        "default-runtime": "nvidia",
        "insecure-registries": [
            "10.255.0.58:9500"
        ]
    }
    EOF

    mkdir -p /etc/systemd/system/docker.service.d

    systemctl daemon-reload
    systemctl restart docker
fi

# sudo usermod -aG docker $USER
# newgrp docker

docker version
