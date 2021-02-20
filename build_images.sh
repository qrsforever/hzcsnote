#!/bin/bash
export LANG="en_US.utf8"

VENDOR=hzcsai_com

MAJOR_K12AI=1
MINOR_K12AI=1

DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
VERSION=$(git describe --tags --always)
URL=$(git config --get remote.origin.url)
COMMIT=$(git rev-parse HEAD | cut -c 1-7)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
NUMBER=$(git rev-list HEAD | wc -l | awk '{print $1}')

echo "DATE: $DATE"
echo "VERSION: $VERSION"
echo "URL: $URL"
echo "COMMIT: $COMMIT"
echo "BRANCH: $BRANCH"
echo "NUMBER: $NUMBER"

__build_notebook() 
{

    if [[ ! -d .jupyter_config ]]
    then
        git clone https://gitee.com/lidongai/jupyter_config.git .jupyter_config
    fi
    REPOSITORY=$VENDOR/k12nb
    docker build --tag $REPOSITORY --file Dockerfile .
}

__main()
{
    __build_notebook
}

__main $@
