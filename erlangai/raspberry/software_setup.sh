
#!/bin/bash

USER_HOME=/home/$USER
CUDA_HOME=/usr/local/cuda

PIP_INSTALL="sudo pip3 install --retries 10 --timeout 120"
APT_INSTALL="sudo apt install -y --no-install-recommends"
BOOTRC_FILE="${USER_HOME}/.bootrc'
HOST_ADDR=`who | grep "pts/0" | awk -F" " '{match($NF, /[^(].*[^)]/); print substr($NF, RSTART,RLENGTH)}'`

echo_bootrc() {
    echo "$*" | tee -a $BOOTRC_FILE
}

echo_bashrc() {
    echo "$*" | tee -a ${USER_HOME}/.bashrc
}

# on boot script
__setup_bootrc() {
    echo -e "#!/bin/bash\nsleep 10" > $BOOTRC_FILE
    chmod 777 $BOOTRC_FILE
    sudo bash -c "echo '@reboot  root  test -x ${BOOTRC_FILE} && ${BOOTRC_FILE}' >> /etc/crontab"
}

# environment
__setup_bashrc() {
    echo_bashrc "alias pip='pip3'"
    echo_bashrc "alias python='python3'"
    echo_bashrc "export PIP_INSTALL='${PIP_INSTALL}'"
    echo_bashrc "export APT_INSTALL='${APT_INSTALL}'"
    echo_bashrc "export CUDA_HOME=${CUDA_HOME}"
}

# mount.nfs host
__setup_mntnfs(){
    mkdir -p ${USER_HOME}/omega
    ${APT_INSTALL} nfs-common
    echo_bootrc "mount.nfs ${HOST_ADDR}:/blog/public ${USER_HOME}/omega"
}

# notebook
__setup_notebook() {
    ${PIP_INSTALL} watermark autopep8
    ${PIP_INSTALL} jupyter jupyter_contrib_nbextensions jupyter_nbextensions_configurator
    sudo jupyter contrib nbextension install --sys-prefix
    sudo jupyter nbextensions_configurator enable
    git clone --depth 1 https://github.com.cnpmjs.org/qrsforever/jupyter_config.git
    sudo ./jupyter_config/install.sh
    echo_bootrc "su - $USER -c 'umask 0000; jupyter notebook --no-browser --notebook-dir=${USER_HOME}/omega --allow-root --ip=0.0.0.0 --port=8118 &'"
}

# cmake
__setup_cmake() {
    wget https://github.com/Kitware/CMake/releases/download/v3.21.2/cmake-3.21.2-linux-aarch64.tar.gz
    tar zxf cmake-3.21.2-linux-aarch64.tar.gz
    cp -aprf cmake-3.21.2-linux-aarch64.tar/* /usr/
}

# machine learning
__setup_ml() {
    # tensorflow
    ${APT_INSTALL} libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
    ${PIP_INSTALL} -U pip testresources setuptools==49.6.0
    ${APT_INSTALL} --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 tensorflow
    
    # onnx2tensor
    ${APT_INSTALL} libprotobuf-dev protobuf-compiler
    git clone --depth 1 --recursive https://github.com.cnpmjs.org/onnx/onnx-tensorrt.git
    cd onnx-tensorrt && mkdir build && cd build && cmake ../ && make -j && sudo make install
    
    # pycuda, onnx_helper
    ${PIP_INSTALL} --global-option=build_ext --global-option="-I${CUDA_HOME}/include/" --global-option="-L${CUDA_HOME}/lib" pycuda
    git clone --depth 1 https://github.com.cnpmjs.org/NVIDIA/TensorRT.git
}

__setup_bootrc
__setup_bashrc
__setup_mntnfs
