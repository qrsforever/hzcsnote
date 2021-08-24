#!/bin/bash

for image_uri in $(kubeadm config images list)
do
    echo "pull $image_uri ..."
    exist=`docker image ls $image_uri  --format "{{.Tag}}"`
    if [[ x$exist == x ]]
    then
        image_name=`echo $image_uri | cut -d\/ -f2-`
        # image_name=`echo $image_uri | rev | cut -d\/ -f1 | rev`
        name=${image_name%%:*}
        if [[ ${name} == "coredns/coredns" ]]
        then
            version=${image_name##*:v}
            docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:${version}
            docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:${version} k8s.gcr.io/${image_name}
            docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:${version}
        else
            docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/$image_name
            docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/$image_name k8s.gcr.io/$image_name
            docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/$image_name
        fi
    fi
done
