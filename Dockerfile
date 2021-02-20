FROM ufoym/deepo:1.8.0.dev20210103

LABEL org.label-schema.name="k12nb"

ARG jupyter_data_dir=/root/.local/share/jupyter
ARG jupyter_conf_dir=/root/.jupyter

ENV TZ=Asia/Shanghai \
    LC_ALL=C.UTF-8 \
    PYTHONIOENCODING=utf-8

WORKDIR /hzcsk12

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="pip install -U --no-cache-dir --retries 20 --timeout 120 \
        --trusted-host mirrors.intra.didiyun.com \
        --index-url http://mirrors.intra.didiyun.com/pip/simple" && \
    sed -i 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//http:\/\/mirrors\.intra\.didiyun\.com\/ubuntu\//g' /etc/apt/sources.list && \
    apt-get update --fix-missing && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        iputils-ping tree jq net-tools \
        tzdata \
        graphviz xvfb \
        ffmpeg \
        python3-opengl \
        && \
    pip uninstall enum34 -y && \
    $PIP_INSTALL \
        GPUtil psutil \
        crontabs redis flask flask_cors h5py protobuf-compiler \
        torchsummary seaborn \
        minio onnx onnxruntime netron pydotplus \
        ipywidgets torchviz pydot graphviz cairosvg \
        statsmodels pyhocon protobuf "jsonnet>=0.10.0" \
        zerorpc python-consul \
        tfrecord plotly opencv-python imutils \
        watermark xlrd xgboost

RUN pip install  --retries 20 --timeout 120 \
        --trusted-host mirrors.aliyun.com \
        --index-url https://mirrors.aliyun.com/pypi/simple/ \
        pytorch-forecasting

RUN PIP_INSTALL="pip install -U --no-cache-dir --retries 20 --timeout 120 \
        --trusted-host pypi.tuna.tsinghua.edu.cn \
        --index-url https://pypi.tuna.tsinghua.edu.cn/simple" && \
    $PIP_INSTALL \
        detectron2 \
        jupyter \
        jupyter_contrib_nbextensions \
        jupyter_nbextensions_configurator \
        && \
    jupyter contrib nbextension install --sys-prefix && \
    jupyter nbextensions_configurator enable && \
    mkdir -p ${jupyter_data_dir}/nbextensions && \
    mkdir -p ${jupyter_conf_dir}/nbconfig && \
    jupyter notebook --generate-config -y

RUN jupyter nbextension enable vim_binding/vim_binding && \
    jupyter nbextension enable jupyter-js-widgets/extension && \
    jupyter nbextension enable execute_time/ExecuteTime && \
    jupyter nbextension enable snippets_menu/main && \
    jupyter nbextension enable table_beautifier/main && \
    jupyter nbextension enable skip-traceback/main && \
    jupyter nbextension enable toc2/main

COPY .jupyter_config/jupyter_notebook_config.json ${jupyter_conf_dir}/jupyter_notebook_config.json
COPY .jupyter_config/notebook.json ${jupyter_conf_dir}/nbconfig/notebook.json
COPY .jupyter_config/vim_binding ${jupyter_data_dir}/nbextensions/vim_binding

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["/bin/bash"]
