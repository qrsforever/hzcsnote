#!/bin/bash
#=================================================================
# date: 2021-02-20 18:31:43
# title: start_notebook
# author: QRS
#=================================================================

export LANG="en_US.utf8"

CUR_FIL=${BASH_SOURCE[0]}
TOP_DIR=`cd $(dirname $CUR_FIL); pwd`
DST_DIR='/hzcsk12'

VENDOR=hzcsai_com

K12NB_PROJECT=k12nb
K12NB_PORT=8118
K12NB_WWW_PORT=9091

K12PYR_PROJECT=k12pyr
K12PYR_PORT=8178

MINIO_SERVER_URL='s3-internal.didiyunapi.com'
MINIO_ACCESS_KEY='AKDD002E38WR1J7RMPTGRIGNVCVINY'
MINIO_SECRET_KEY='ASDDXYWs45ov7MNJbj5Wc2PM9gC0FSqCIkiyQkVC'


__start_notebook()
{
    PROJECT=$1
    PORT=$2
    REPOSITORY=$VENDOR/$PROJECT
    JNAME=k12nb

    check_exist=`docker container ls --filter name=${JNAME} --filter status=running -q`
    echo "docker container ls --filter name=${JNAME} --filter status=running -q"
    if [[ x$check_exist == x ]]
    then
        SOURCE_NOTE_DIR=$TOP_DIR
        TARGET_NOTE_DIR=$DST_DIR/hzcsnote
        if [[ $PROJECT == $K12NB_PROJECT ]]
        then
            echo "start http.sever"
            cd $SOURCE_NOTE_DIR/k12libs/www
            ./run.sh
            cd - >/dev/null
            xvfb_args="xvfb-run -a -s \"-screen 0 1400x900x24\""
        else
            xvfb_args=""
        fi
        docker run -dit --runtime nvidia --name ${JNAME} --restart unless-stopped --shm-size 10g \
            --volume $SOURCE_NOTE_DIR:$TARGET_NOTE_DIR \
            --entrypoint /bin/bash ${@:3:$#} --network host --hostname ${JNAME} ${REPOSITORY} \
            -c "umask 0000; jupyter notebook --no-browser --notebook-dir=$TARGET_NOTE_DIR --allow-root --ip=0.0.0.0 --port=$PORT"
            # -c "umask 0000; $xvfb_args jupyter notebook --no-browser --notebook-dir=$TARGET_NOTE_DIR --allow-root --ip=0.0.0.0 --port=$PORT"
    else
        echo "$JNAME: already run!!!"
    fi
}


__main()
{
    __start_notebook $K12NB_PROJECT $K12NB_PORT \
        --env PYTHONPATH=$DST_DIR/hzcsnote \
        --env MINIO_SERVER_URL=$MINIO_SERVER_URL \
        --env MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY \
        --env MINIO_SECRET_KEY=$MINIO_SECRET_KEY \
        --volume /data:/data \
        --volume /data/kaggle:/kaggle \
        --volume /raceai:/raceai \
        --volume $TOP_DIR/.jupyter_config/etc/netrc:/root/.netrc \
        --volume $TOP_DIR/.jupyter_config/jupyter:/root/.jupyter \
        --volume $TOP_DIR/.jupyter_config/local/share/jupyter:/root/.local/share/jupyter \
        --volume /data/pretrained/cv:/root/.cache/torch/hub/checkpoints
}

__main $*
