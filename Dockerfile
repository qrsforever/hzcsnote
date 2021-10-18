FROM hzcsai_com/k12ai

LABEL org.label-schema.name="k12nb"

ARG jupyter_data_dir=/root/.local/share/jupyter
ARG jupyter_conf_dir=/root/.jupyter

RUN apt-get update --fix-missing && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        iputils-ping tree jq net-tools \
        tzdata \
        graphviz xvfb \
        ffmpeg \
        python3-opengl \
        && \
    $PIP_INSTALL \
        GPUtil psutil minio \
        crontabs redis flask flask_cors h5py protobuf-compiler \
        sklearn torchsummary seaborn hiddenlayer \
        tensorflow-cpu tf2onnx netron pydotplus \
        onnx onnxruntime onnxoptimizer onnx-simplifier \
        ipywidgets torchviz pydot graphviz cairosvg \
        statsmodels pyhocon protobuf "jsonnet>=0.10.0" \
        zerorpc python-consul \
        tfrecord plotly opencv-python imutils \
        watermark xlrd xgboost moviepy --use-deprecated=legacy-resolver 

RUN pip install  --retries 20 --timeout 120 \
        --trusted-host mirrors.aliyun.com \
        --index-url https://mirrors.aliyun.com/pypi/simple/ \
        pytorch-forecasting

RUN PIP_INSTALL="pip install -U --no-cache-dir --retries 20 --timeout 120 \
        --trusted-host pypi.tuna.tsinghua.edu.cn \
        --index-url https://pypi.tuna.tsinghua.edu.cn/simple" && \
    $PIP_INSTALL \
        autopep8 \
        notebook==v6.4.4 \
        jupyter \
        jupyter_contrib_nbextensions \
        jupyter_nbextensions_configurator \
        && \
    jupyter contrib nbextension install --sys-prefix && \
    jupyter nbextensions_configurator enable && \
    mkdir -p ${jupyter_data_dir}/nbextensions && \
    mkdir -p ${jupyter_conf_dir}/nbconfig && \
    jupyter notebook --generate-config -y

# RUN jupyter nbextension enable vim_binding/vim_binding && \
#     jupyter nbextension enable jupyter-js-widgets/extension && \
#     jupyter nbextension enable execute_time/ExecuteTime && \
#     jupyter nbextension enable snippets_menu/main && \
#     jupyter nbextension enable table_beautifier/main && \
#     jupyter nbextension enable skip-traceback/main && \
#     jupyter nbextension enable toc2/main

# Using volumn map
# COPY .jupyter_config/jupyter_notebook_config.json ${jupyter_conf_dir}/jupyter_notebook_config.json
# COPY .jupyter_config/notebook.json ${jupyter_conf_dir}/nbconfig/notebook.json
# COPY .jupyter_config/vim_binding ${jupyter_data_dir}/nbextensions/vim_binding

CMD ["/bin/bash"]
