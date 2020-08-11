#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file nb_global_env.py
# @brief
# @author QRS
# @version 1.0
# @date 2019-12-06 12:16:50

from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Sequence # noqa
import sys
import os
import base64
import hashlib
import requests
import logging
import json
import _jsonnet
import consul
import errno
import time
import socket
import shlex
import shutil
import threading
import multiprocessing
from multiprocessing.queues import Empty
from flask import Flask, request
from flask_cors import CORS

from IPython.display import clear_output, display, HTML, IFrame
from .nb_widget import K12WidgetGenerator
import ipywidgets as widgets

import signal
from tensorboard import notebook as tbnotebook
from tensorboard import manager as tbmanager

import matplotlib.pyplot as plt # noqa
# from matplotlib.ticker import MultipleLocator

from abc import ABC, abstractmethod

from collections import OrderedDict
import torch
import torchvision
import pytorch_lightning as pl
from torch import optim
import torch.nn as nn
from PIL import Image
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import (Dataset, DataLoader)

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True
# Access-Control-Allow-Origin
CORS(app, supports_credentials=True)

# Global
g_queue = None
g_flask_process = None
g_result_process = None
g_contexts = {}


def get_host_ip():
    ip = ''
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_net_ip():
    result = os.popen('curl -s http://txt.go.sohu.com/ip/soip| grep -P -o -i "(\d+\.\d+.\d+.\d+)"', 'r') # noqa
    if result:
        return result.read().strip('\n')
    return None

host = get_host_ip()
port = 8119

flask_host = host
flask_port = 8117

consul_addr = get_net_ip()
consul_port = 8500

netip = consul_addr

NBURL = 'http://{}:{}'.format(netip, 8118) # Jupyter
AIURL = 'http://{}:{}'.format(host, 8119) # K12AI API
SSURL = 'http://{}:{}'.format(netip, 8500) # Consul
TBURL = 'http://{}:{}'.format(host, 6006) # Tensorboard
DSURL = 'http://{}:{}'.format(netip, 9090) # Dataset
W3URL = 'http://{}:{}'.format(netip, 9091) # Model Diagram

K12AI_HOST_ADDR = host
K12AI_WLAN_ADDR = consul_addr

## DIR
K12AI_DATASETS_ROOT = '/data/datasets'
K12AI_USERS_ROOT = '/data/users'
K12AI_TBLOG_ROOT = '/data/tblogs'
K12AI_PRETRAINED_ROOT = '/data/pretrained'
K12AI_NBDATA_ROOT = '/data/nb_data'


def k12ai_set_notebook(cellw=None):
    if cellw:
        display(HTML('<style>.container { width:%d%% !important; }</style>' % cellw))

def k12ai_restart_kernel() :
    display(HTML("<script>Jupyter.notebook.kernel.restart()</script>"))

def k12ai_start_tensorboard(port, logdir, clear=False, reload_interval=10, height=None, display=True):
    # kill
    infos = tbmanager.get_all()
    for info in infos:
        if info.port != port:
            continue
        try:
            os.kill(info.pid, signal.SIGKILL)
        except Exception:
            pass
        infofile = os.path.join(tbmanager._get_info_dir(), f'pid-{info.pid}.info')
        try:
            os.unlink(infofile)
        except OSError as e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise
        break

    # start
    if clear and os.path.exists(logdir):
        shutil.rmtree(logdir, ignore_errors=True)
        os.mkdir(logdir)

    strargs = f'--host {K12AI_HOST_ADDR} --port {port} --logdir {logdir} --reload_interval {reload_interval}'
    command = shlex.split(strargs, comments=True, posix=True)
    tbmanager.start(command)

    # display
    if display:
        tbnotebook.display(port, height)

    return f'http://{K12AI_WLAN_ADDR}:{port}'

def k12ai_start_html(uri, width=None, height=None):
    k12ai_set_notebook(cellw=95)
    if width is None:
        width = '100%'
    if height is None:
        height = 300
    return IFrame(uri, width=width, height=height)

def _print_json(text, indent):
    if isinstance(text, str):
        print(json.dumps(json.loads(text), indent=indent, ensure_ascii=False))
    else:
        print(json.dumps(text, indent=indent, ensure_ascii=False))

def k12ai_print(text, indent=4):
    if not text:
        return
    return _print_json(text, indent)

def k12ai_count_down(secs):
    seq = list(range(secs))

    def _time_down(seq):
        seq.pop()
        time.sleep(1)
        return 0 == len(seq)
    return lambda x=seq: _time_down(x)

def k12ai_get_top_dir():
    return os.path.abspath(
                os.path.dirname(os.path.abspath(__file__)) + '../../..')

def k12ai_get_app_dir(svr):
    return os.path.join(k12ai_get_top_dir(), svr, 'app')

def k12ai_post_request(uri, data):
    api = 'http://%s:%d/%s' % (host, port, uri)
    if isinstance(data, str):
        return requests.post(url=api, json=json.loads(data)).text
    if isinstance(data, dict):
        return requests.post(url=api, json=data).text
    return None

def k12ai_get_data(key, subkey=None, num=1, waitcnt=1, rm=False, http=False):
    if subkey:
        key = '%s/%s' % (key, subkey)
    if waitcnt < 0:
        waitcnt = 999999
    if http:
        result = os.popen('curl http://{}:{}/v1/kv/{}'.format(consul_addr, consul_port, key), 'r')
        try:
            body = json.loads(result.read())
            data = base64.b64decode(body[0]['Value'])
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            return None
        except Exception as err:
            raise err
    else:
        client = consul.Consul(consul_addr, consul_port)
        i = 0
        try:
            while i < waitcnt:
                _, data = client.kv.get(key, recurse=True)
                if not data:
                    i = i + 1
                    time.sleep(1)
                    continue
                if len(data) < num:
                    num = len(data)
                out = []
                for item in data[-num:]:
                    out.append({
                        'key': item['Key'],
                        'value': json.loads(str(item['Value'], encoding='utf-8'))
                        })
                if rm:
                    client.kv.delete(key, recurse=True)
                return out
        except KeyboardInterrupt:
            print("Interrupted!")
        return None

def k12ai_del_data(key, http=False):
    if http:
        result = os.popen('curl --request DELETE http://{}:{}/v1/kv/{}'.format(
            consul_addr, consul_port, key), 'r')
        if result:
            if json.loads(result.read()):
                return 'success'
        return 'fail'
    else:
        client = consul.Consul(consul_addr, consul_port)
        client.kv.delete(key, recurse=True)
        return 'success'

def k12ai_get_error_data(datakey, num=1):
    return k12ai_get_data(datakey, 'error', num)

def k12ai_get_metrics_data(datakey, num=1):
    return k12ai_get_data(datakey, 'metrics', num)

def k12ai_out_data(key, contents, hook_func = None):
    tab = widgets.Tab(layout={'width': '100%'})
    children = [widgets.Output(layout={
        'border': '1px solid black',
        'min_height': '200px'}) for name in contents]
    tab = widgets.Tab()
    tab.children = children
    for i, title in enumerate(contents):
        tab.set_title(i, title)
    display(tab)

    try:
        while True:
            for i, title in enumerate(contents):
                result = k12ai_get_data(key, title)
                if result is not None:
                    with children[i]:
                        children[i].clear_output()
                        k12ai_print(result)
            if not hook_func:
                break
            if hook_func():
                break
    except KeyboardInterrupt:
        print("Interrupted!")

def k12ai_post_cv_request(uri, op, user, uuid, params=None):
    if not params:
        params = '{}'
    if isinstance(params, dict):
        params = json.dumps(params)
    data = json.loads('''{
        "token": "123456",
        "op":"%s",
        "user": "%s",
        "service_name": "k12cv",
        "service_uuid": "%s",
        "service_params": %s
    }''' % (op, user, uuid, params))
    api = 'http://%s:%d/%s' % (host, port, uri)
    key = 'framework/%s/%s/%s' % (user, uuid, op.split('.')[0])
    return {'req': data,
            'res': json.loads(requests.post(url=api, json=data).text),
            'key': key}

def k12ai_post_nlp_request(uri, op, user, uuid, params=None):
    if not params:
        params = '{}'
    if isinstance(params, dict):
        params = json.dumps(params)
    data = json.loads('''{
        "token": "123456",
        "op":"%s",
        "user": "%s",
        "service_name": "k12nlp",
        "service_uuid": "%s",
        "service_params": %s
    }''' % (op, user, uuid, params))
    api = 'http://%s:%d/%s' % (host, port, uri)
    key = 'framework/%s/%s/%s' % (user, uuid, op.split('.')[0])
    return {'req': data,
            'res': json.loads(requests.post(url=api, json=data).text),
            'key': key}

def k12ai_json_load(path):
    if not os.path.exists(path):
        raise RuntimeError('not found file: %s' % path)
    str = ''
    with open(path, 'r') as f:
        str = json.load(f)
    return str

### Train

@app.route('/k12ai/notebook/message', methods=['POST', 'GET'])
def _http_handle():
    try:
        reqjson = json.loads(request.get_data().decode())
        msgtype = reqjson['msgtype']
        if msgtype == 'protodata':
            tag = reqjson['tag']
            ctx = g_contexts.get(tag, None)
            if ctx:
                ctx.protodata = reqjson[msgtype]['datastr']
        elif msgtype == 'genpycode':
            net_def = reqjson['net_def']
            sys.path.append(k12ai_get_app_dir('cv'))
            from vulkan.builders.net_builder import NetBuilder
            net = NetBuilder(net_def).build_net()
            net.write_net('/tmp/net_def.py')
            sys.path.remove(k12ai_get_app_dir('cv'))
            with open('/tmp/net_def.py', 'r') as fr:
                response = {'pycode': str(fr.read())}
                return json.dumps(response)
    except Exception as err:
        err = {'error': format(err)}
        return json.dumps(err)
    return ''

def _start_work_process(context):
    global g_queue, g_result_process, g_contexts

    if not g_queue:
        g_queue = multiprocessing.Queue()

    def _queue_work():
        context = None
        key = None
        timeout = 3
        total_count = 0
        result = {}
        while True:
            try:
                tag, key, flag = g_queue.get(True, timeout=timeout)
                context = g_contexts.get(tag, None)
                if flag == 1:
                    with context.progress.output:
                        clear_output()
                    timeout = 3
                    total_count = 0
                    result = {}
                    continue
                elif flag == 2:
                    timeout = 5
                elif flag == 3:
                    context.progress.trainstart.disabled = False
                    context.progress.trainstop.disabled = True
                    context.progress.value = 100.0
                    context.progress.description = '100.0%'
                    timeout = 300
                    continue
                elif flag == 9:
                    timeout = 1
                    continue
                else:
                    timeout = 3
            except Empty:
                pass
            except AttributeError:
                pass

            if not context or not key:
                continue

            total_count += 1
            if total_count % 2 == 0:
                context.progress.description = str(context.progress.value) + '%'
            else:
                context.progress.description = 'Progress:'

            try:
                # error
                result['error'] = {}
                data = k12ai_get_data(key, 'error', num=1)
                if data:
                    result['error'] = data[0]['value']
                    code = result['error']['data']['code']
                    # 100003: finish 100004: stop
                    if code == 100003 or code == 100004 or code > 100100:
                        g_queue.put((context.tag, key, 3))

                # metrics
                if context.progress.phase == 'train':
                    data = k12ai_get_data(key, 'metrics', num=1, rm=True)
                    if data:
                        result['metrics'] = data[0]['value']
                        if context.framework == 'k12ml':
                            context.progress.value = 1.0
                        else:
                            for obj in result['metrics']['data']:
                                if obj['type'] == 'scalar':
                                    if 'progress' in obj['data']['title']:
                                        progress = obj['data']['payload']['y'][0]['value']
                                        context.progress.value = progress
                else: # context.progress.phase == 'evaluate':
                    data = k12ai_get_data(key, 'metrics', num=10, rm=True)
                    if data:
                        result['metrics'] = data[-1]['value']
                        context.progress.value = result['metrics']['data']['progress']
            except Exception:
                pass

            if len(result) > 0:
                if 'error' in result:
                    context._output(result['error'])
                if 'metrics' in result:
                    with context.progress.output:
                        clear_output(wait=True)
                        k12ai_print(result['metrics'])

    if not g_result_process or not g_result_process.is_alive():
        g_result_process = threading.Thread(target=_queue_work, args=())
        g_result_process.start()
        time.sleep(1.5)


def _init_project_schema(context, params):
    context._output('----------Generate Project Schema (take a monment: 5s)--------------')
    context._output(params, 0)

    context.user = params.get('project.user', '16601548608')
    context.framework = params.get('project.framework', None)
    context.task = params.get('project.task', None)
    context.network = params.get('project.network', None)
    context.dataset = params.get('project.dataset', None)
    context.tag = '%s_%s_%s' % (context.task, context.network, context.dataset)
    context.uuid = hashlib.md5(context.tag.encode()).hexdigest()[0:6]
    context.usercache = f'{K12AI_USERS_ROOT}/{context.user}/{context.uuid}'
    context.tb_logdir = f'{K12AI_TBLOG_ROOT}/{context.user}/{context.uuid}'
    context.dataset_dir = f'{K12AI_DATASETS_ROOT}/{context.framework[3:]}/{context.dataset}'
    context.dataset_url = f'{DSURL}'

    g_contexts[context.tag] = context

    response = json.loads(k12ai_post_request(
        uri='k12ai/framework/schema',
        data={
            'service_name': context.framework,
            'service_task': context.task,
            'dataset_name': context.dataset,
            'network_type': context.network
            }))

    if response['code'] != 100000:
        context._output(response)
        return

    if context.tb_port:
        k12ai_set_notebook(cellw=95)
        tb_url = k12ai_start_tensorboard(context.tb_port, context.tb_logdir, clear=False, display=False)
    else:
        tb_url = None

    if context.model_templ:
        context.templ_params = f'jfile={context.model_templ}&flask=http://{netip}:{flask_port}/k12ai/notebook/message&tag={context.tag}'
        global g_flask_process
        if g_flask_process is None or not g_flask_process.is_alive():
            def _run_flask(*args, **kwargs):
                try:
                    app.run(*args, **kwargs)
                except Exception:
                    pass
            g_flask_process = threading.Thread(target=_run_flask,
                    kwargs={"host": flask_host, "port": flask_port})
            g_flask_process.start()

    context.parse_schema(json.loads(response['data']), tb_url=tb_url)


def _on_project_confirm(wdg):
    if not hasattr(wdg, 'context'):
        return
    context = wdg.context
    _init_project_schema(context, context.get_all_kv())


def _on_project_trainstart(wdg):
    if not hasattr(wdg, 'progress'):
        return
    context = wdg.progress.context

    if not hasattr(wdg.progress, 'running'):
        wdg.progress.value = 0

    if not hasattr(context, 'user'):
        context._output('start error, no context.user')
        return

    response = json.loads(k12ai_post_request(
            uri='k12ai/platform/stats',
            data={
                'op': 'query',
                'user': context.user,
                'service_uuid': context.uuid,
                'service_params': {'services': True},
                'async': False}))
    if response['code'] != 100000:
        context._output(response)
        return

    if len(response['data']['services']) == 1:
        op = response['data']['services'][0]['op']
        if op != f'{wdg.phase}.start':
            context._output(f'op {op} is running, please stop!')
            return

    op = f'{wdg.phase}.start'
    data = {
        'token': '123456',
        'op': op,
        'user': context.user,
        'service_name': context.framework,
        'service_uuid': context.uuid,
        'service_params': context.get_all_kv()
    }

    response = json.loads(k12ai_post_request(uri='k12ai/framework/execute', data=data))
    wdg.progress.trainstart.disabled = True
    wdg.progress.trainstop.disabled = False
    context._output(response)
    if response['code'] != 100000:
        return
    k12ai_start_tensorboard(context.tb_port, context.tb_logdir, clear=True, display=False)
    context.progress = wdg.progress
    key = 'framework/%s/%s/%s' % (context.user, context.uuid, wdg.phase)
    k12ai_del_data(key)
    _start_work_process(context)
    g_queue.put((context.tag, key, 1))


def _on_project_trainstop(wdg):
    if not hasattr(wdg, 'progress'):
        return
    context = wdg.progress.context
    if not hasattr(context, 'user'):
        context._output('stop error, no context.user')
        return

    op = f'{wdg.phase}.stop'
    data = {
        'token': '123456',
        'op': op,
        'user': context.user,
        'service_name': context.framework,
        'service_uuid': context.uuid,
        }
    response = json.loads(k12ai_post_request(uri='k12ai/framework/execute', data=data))
    wdg.progress.trainstart.disabled = False
    wdg.progress.trainstop.disabled = True
    context._output(response)
    if response['code'] != 100000:
        return
    key = 'framework/%s/%s/%s' % (context.user, context.uuid, wdg.phase)
    g_queue.put((context.tag, key, 2))


def _on_project_traininit(context, phase, wdg_start, wdg_stop, wdg_progress, wdg_output):
    wdg_start.on_click(_on_project_trainstart)
    wdg_stop.on_click(_on_project_trainstop)

    wdg_start.progress = wdg_progress
    wdg_stop.progress = wdg_progress
    wdg_output.progress = wdg_progress

    wdg_start.phase = phase
    wdg_stop.phase = phase
    wdg_progress.phase = phase

    wdg_progress.trainstart = wdg_start
    wdg_progress.trainstop = wdg_stop
    wdg_progress.output = wdg_output
    wdg_progress.context = context

    context.progress = wdg_progress

    response = json.loads(k12ai_post_request(
            uri='k12ai/platform/stats',
            data= {
                'op': 'query',
                'user': context.user,
                'service_uuid': context.uuid,
                'service_params': {'services': True},
                'async': False}))
    if response['code'] != 100000:
        context._output(response)
        return
    if len(response['data']['services']) == 1:
        op = response['data']['services'][0]['op']
        if op == f'{phase}.start':
            wdg_start.disabled = True
            wdg_stop.disabled = False
            _start_work_process(context)
            key = 'framework/%s/%s/%s' % (context.user, context.uuid, phase)
            g_queue.put((context.tag, key, 1))
    else:
        wdg_start.disabled = False
        wdg_stop.disabled = True

def k12ai_run_project(lan='en', debug=False, tb_port=None,
        framework=None, task=None, network=None, dataset=None, model_templ=None):
    if task is None:
        events = {
                'project.confirm': _on_project_confirm,
                'project.train.init': _on_project_traininit,
                }
        pro_schema = os.path.join(k12ai_get_top_dir(), 'k12libs/templates', 'projects.jsonnet')
        context = K12WidgetGenerator(lan, debug=debug, tb_port=tb_port, events=events)
        context.parse_schema(json.loads(_jsonnet.evaluate_file(
            pro_schema, tla_vars={'framework': 'k12cv' if framework is None else framework})))
    else:
        events = {
                'project.train.init': _on_project_traininit,
                }
        context = K12WidgetGenerator(lan, debug=debug, tb_port=tb_port, events=events)
        if task is None:
            task = 'cls' if framework == 'k12cv' else 'sa'
        if dataset is None:
            dataset = 'cifar10' if framework == 'k12cv' else 'sst'
        if network is None:
            raise RuntimeError('network is null')
        if model_templ:
            context.model_templ = model_templ
        _init_project_schema(context, {
            'project.framework': framework,
            'project.task': task,
            'project.network': network,
            'project.dataset': dataset,
        })
    display(context.page)
    return context


def k12ai_get_schema(framework, task, network, dataset):
    response = json.loads(k12ai_post_request(
        uri='k12ai/framework/schema',
        data={
            'service_name': framework,
            'service_task': task,
            'dataset_name': dataset,
            'network_type': network
        }))
    return json.loads(response['data'])


def k12ai_get_config(framework, task, network, dataset):
    context = K12WidgetGenerator()
    context.parse_schema(k12ai_get_schema(framework, task, network, dataset))
    return context.get_all_kv()


def k12ai_get_tooltips(framework, task, network, dataset):
    context = K12WidgetGenerator()
    return context.parse_schema(k12ai_get_schema(framework, task, network, dataset), tooltips=True)


def k12ai_train_execute(user='15801310416', framework='k12cv', task='cls', network='resnet50',
        dataset='Boats', batchsize=32, inputsize=32, epoch_num=1, log_iters=None, test_iters=None, run_num=1):
    config = k12ai_get_config(framework, task, network, dataset)
    if framework == 'k12cv':
        config['train.batch_size'] = batchsize
        config['val.batch_size'] = batchsize
        config['test.batch_size'] = batchsize
        config['train.data_transformer.input_size'] = [inputsize, inputsize]
        config['val.data_transformer.input_size'] = [inputsize, inputsize]
        config['test.data_transformer.input_size'] = [inputsize, inputsize]
        config['solver.lr.metric'] = 'epoch'
        config['solver.max_epoch'] = epoch_num
        if log_iters:
            config['solver.display_iter'] = log_iters
        if test_iters:
            config['solver.test_interval'] = test_iters
    user = user
    tag = hashlib.md5(f'{task}{network}{dataset}{batchsize}{inputsize}'.encode()).hexdigest()[0:6]
    keys = []
    for i in range(run_num):
        uuid = f'{tag}-{i}'
        data = {
            'token': tag,
            'op': 'train.start',
            'user': user,
            'service_name': framework,
            'service_uuid': uuid,
        }
        data['op'] = 'train.stop'
        k12ai_post_request(uri='k12ai/framework/execute', data=data)

        time.sleep(0.5)

        data['op'] = 'train.start'
        data['service_params'] = config
        k12ai_post_request(uri='k12ai/framework/execute', data=data)

        keys.append(f'framework/{user}/{uuid}/train')
    return keys


############################### Easyai ###################################

from torchvision.transforms import ( # noqa
        Resize,
        Compose,
        ToTensor,
        Normalize,
        RandomOrder,
        ColorJitter,
        RandomRotation,
        RandomGrayscale,
        RandomResizedCrop,
        RandomVerticalFlip,
        RandomHorizontalFlip)

class IDataTransforms(object):

    @staticmethod
    def compose_order(transforms: List):
        return Compose(transforms)

    @staticmethod
    def shuffle_order(transforms: List):
        return RandomOrder(transforms)

    @staticmethod
    def image_resize(size):
        return Resize(size=size)

    @staticmethod
    def image_to_tensor():
        return ToTensor()

    @staticmethod
    def normalize_tensor(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)):
        return Normalize(mean, std)

    @staticmethod
    def random_brightness(factor=0.25):
        return ColorJitter(brightness=factor)

    @staticmethod
    def random_contrast(factor=0.25):
        return ColorJitter(contrast=factor)

    @staticmethod
    def random_saturation(factor=0.25):
        return ColorJitter(saturation=factor)

    @staticmethod
    def random_hue(factor=0.25):
        return ColorJitter(hue=factor)

    @staticmethod
    def random_rotation(degrees=25):
        return RandomRotation(degrees=degrees)

    @staticmethod
    def random_grayscale(p=0.5):
        return RandomGrayscale(p=p)

    @staticmethod
    def random_resized_crop(size):
        return RandomResizedCrop(size=size)

    @staticmethod
    def random_horizontal_flip(p=0.5):
        return RandomHorizontalFlip(p=p)

    @staticmethod
    def random_vertical_flip(p=0.5):
        return RandomVerticalFlip(p=p)


class EasyaiDataset(ABC, Dataset):
    def __init__(self, mean=None, std=None, **kwargs):
        self.mean, self.std = mean, std
        self.augtrans = None
        self.imgtrans = ToTensor()

        # reader
        data = self.data_reader(**kwargs)
        if isinstance(data, (tuple, list)) and len(data) == 2:
            self.images, self.labels = data
        elif isinstance(data, dict) and all([x in data.keys() for x in ('images', 'labels')]):
            self.images, self.labels = data['images'], data['labels']
        else:
            raise ValueError('The return of data_reader must be List or Dict')

    @abstractmethod
    def data_reader(self, **kwargs) -> Union[Tuple[List, List, List], Dict[str, List]]:
        """
        (M)
        """

    def set_aug_trans(self, transforms:Union[list, None], random_order=False):
        if transforms:
            if any([not hasattr(x, '__call__') for x in transforms]):
                raise ValueError(f'set_aug_trans: transforms params is invalid.')
            if random_order:
                self.augtrans = RandomOrder(transforms)
            else:
                self.augtrans = Compose(transforms)

    def set_img_trans(self, input_size:Union[Tuple[int, int], int, None], normalize=True):
        trans = []
        if input_size:
            trans.append(Resize(input_size))
        trans.append(ToTensor())
        if normalize and self.mean and self.std:
            trans.append(Normalize(mean=self.mean, std=self.std))
        self.imgtrans = Compose(trans)

    def __getitem__(self, index):
        img = Image.open(self.images[index]).convert('RGB')
        if self.augtrans:
            img = self.augtrans(img)
        return self.imgtrans(img), self.labels[index], self.images[index]

    def __len__(self):
        return len(self.images)


class EasyaiClassifier(pl.LightningModule, IDataTransforms):
    def __init__(self):
        super(EasyaiClassifier, self).__init__()
        self.model = self.build_model()
        self.criterion = None
        self.datasets = {'train': None, 'val': None, 'test': None}

    def setup(self, stage: str):
        pass

    def teardown(self, stage: str):
        pass

    # Data
    def load_presetting_dataset_(self, dataset_name):
        class JsonfileDataset(EasyaiDataset):
            def data_reader(self, path, phase):
                """
                Args:
                    path: the dataset root directory
                    phase: the json file name (train.json / val.json / test.json)
                """
                image_list = []
                label_list = []
                with open(os.path.join(path, f'{phase}.json')) as f:
                    items = json.load(f)
                    for item in items:
                        image_list.append(os.path.join(path, item['image_path']))
                        label_list.append(item['label'])
                return image_list, label_list

        root = f'{K12AI_DATASETS_ROOT}/cv/{dataset_name}'
        datasets = {
            'train': JsonfileDataset(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5), path=root, phase='train'),
            'val': JsonfileDataset(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5), path=root, phase='val'),
            'test': JsonfileDataset(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5), path=root, phase='test'),
        }
        return datasets

    def prepare_dataset(self) -> Union[EasyaiDataset, List[EasyaiDataset], Dict[str, EasyaiDataset]]:
        return self.load_presetting_dataset_('rmnist')

    @staticmethod
    def _safe_delattr(cls, method):
        try:
            delattr(cls, method)
        except Exception:
            pass

    def prepare_data(self):
        datasets = self.prepare_dataset()
        if isinstance(datasets, EasyaiDataset):
            self._safe_delattr(self.__class__, 'val_dataloader')
            self._safe_delattr(self.__class__, 'validation_step')
            self._safe_delattr(self.__class__, 'validation_epoch_end')
            self._safe_delattr(self.__class__, 'test_dataloader')
            self._safe_delattr(self.__class__, 'test_step')
            self._safe_delattr(self.__class__, 'test_epoch_end')
            self.datasets['train'] = datasets
        elif isinstance(datasets, (list, tuple)) and len(datasets) <= 3:
            self.datasets['train'] = datasets[0]
            self.datasets['val'] = datasets[1]
            if len(datasets) == 2:
                self._safe_delattr(self.__class__, 'test_dataloader')
                self._safe_delattr(self.__class__, 'test_step')
                self._safe_delattr(self.__class__, 'test_epoch_end')
            else:
                self.datasets['test'] = datasets[2]

        elif isinstance(datasets, dict) and \
                all([x in datasets.keys() for x in ('train', 'val', 'test')]):
            self.datasets = datasets
        else:
            raise ValueError('the return of prepare_dataset is invalid.')

    # Model
    def load_pretrained_model_(self, model_name, num_classes=None, pretrained=True):
        model = getattr(torchvision.models, model_name)(pretrained)
        if num_classes:
            if model_name.startswith('vgg'):
                model.classifier[6] = nn.Linear(4096, num_classes)
            elif model_name.startswith('resnet'):
                model.fc = nn.Linear(model.fc.in_features, num_classes)
            elif model_name.startswith('alexnet'):
                model.classifier[6] = nn.Linear(4096, num_classes)
            elif model_name.startswith('mobilenet_v2'):
                model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
            elif model_name.startswith('squeezenet'):
                model.classifier[1] = nn.Conv2d(512, num_classes, kernel_size=1)
            elif model_name.startswith('shufflenet'):
                model.fc = nn.Linear(model.fc.in_features, num_classes)
            elif model_name.startswith('densenet'):
                in_features = {
                    "densenet121": 1024,
                    "densenet161": 2208,
                    "densenet169": 1664,
                    "densenet201": 1920,
                }
                model.classifier = nn.Linear(in_features[model_name], num_classes)
            else:
                raise NotImplementedError(f'{model_name}')
        return model

    def build_model(self):
        return self.load_pretrained_model_('resnet18', 10)

    # Hypes
    @property
    def loss(self):
        if self.criterion is None:
            self.criterion = self.configure_criterion()
        return self.criterion

    def configure_criterion(self):
        # default
        loss = nn.CrossEntropyLoss(reduction='mean')
        return loss

    def configure_optimizer(self):
        # default
        optimizer = optim.Adam(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=0.001)
        return optimizer

    def configure_scheduler(self, optimizer):
        # default
        scheduler = StepLR(optimizer, step_size=30, gamma=0.1)
        return scheduler

    def configure_optimizers(self):
        optimizer = self.configure_optimizer()
        scheduler = self.configure_scheduler(optimizer)
        return [optimizer], [scheduler]

    def forward(self, x, *args, **kwargs):
        return self.model(x)

    def calculate_acc_(self, y_pred, y_true):
        return (torch.argmax(y_pred, axis=1) == y_true).float().mean()

    def step_(self, batch):
        x, y, _ = batch
        y_hat = self.model(x)
        loss = self.loss(y_hat, y)
        return x, y, y_hat, loss

    def get_dataloader(self, phase,
                       data_augment=None, random_order=False,
                       normalize=False, input_size=None,
                       batch_size=32, num_workers=1,
                       drop_last=False, shuffle=False):
        if phase not in self.datasets.keys():
            raise RuntimeError(f'get {phase} data loader  error.')
        dataset = self.datasets[phase]
        dataset.set_aug_trans(transforms=data_augment, random_order=random_order)
        dataset.set_img_trans(input_size=input_size, normalize=normalize)
        return DataLoader(
                dataset,
                batch_size=batch_size,
                num_workers=num_workers,
                drop_last=drop_last,
                shuffle=shuffle)

    ## Train
    def train_dataloader(self) -> DataLoader:
        return self.get_dataloader(
            phase='train',
            data_augment=[
                self.random_resized_crop(size=(128, 128)),
                self.random_brightness(factor=0.3),
                self.random_rotation(degrees=30)
            ],
            random_order=False,
            input_size=128,
            normalize=True,
            batch_size=32,
            num_workers=1,
            drop_last=False,
            shuffle=False)

    def training_step(self, batch, batch_idx):
        x, y, y_hat, loss = self.step_(batch)
        with torch.no_grad():
            accuracy = self.calculate_acc_(y_hat, y)
        log = {'train_loss': loss, 'train_acc': accuracy}
        output = OrderedDict({
            'loss': loss,        # M
            'acc': accuracy,     # O
            'progress_bar': log, # O
            "log": log           # O
        })
        return output

    def training_epoch_end(self, outputs):
        avg_loss = torch.stack([x['loss'] for x in outputs]).mean()
        avg_acc = torch.stack([x['acc'] for x in outputs]).mean()
        log = {'train_loss': avg_loss, 'train_acc': avg_acc}
        return {'progress_bar': log, 'log': log}

    ## Valid
    def val_dataloader(self) -> DataLoader:
        return self.get_dataloader('val',
                input_size=128,
                batch_size=32,
                num_workers=2,
                drop_last=False,
                shuffle=False)

    def validation_step(self, batch, batch_idx):
        x, y, y_hat, loss = self.step_(batch)
        accuracy = self.calculate_acc_(y_hat, y)
        return {'val_loss': loss, 'val_acc': accuracy}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean()
        avg_acc = torch.stack([x['val_acc'] for x in outputs]).mean()
        log = {'val_loss': avg_loss, 'val_acc': avg_acc}
        return {'progress_bar': log, 'log': log}

    ## Test
    def test_dataloader(self) -> DataLoader:
        return self.get_dataloader('test',
                input_size=128,
                batch_size=32,
                num_workers=1,
                drop_last=False,
                shuffle=False)

    def test_step(self, batch, batch_idx):
        x, y, y_hat, loss = self.step_(batch)
        accuracy = self.calculate_acc_(y_hat, y)
        return {'test_loss': loss, 'test_acc': accuracy}

    def test_epoch_end(self, outputs):
        avg_loss = torch.stack([x['test_loss'] for x in outputs]).mean()
        avg_acc = torch.stack([x['test_acc'] for x in outputs]).mean()
        log = {'test_loss': avg_loss, 'test_acc': avg_acc}
        return {'progress_bar': log, 'log': log}


class EasyaiTrainer(pl.Trainer):
    def __init__(self, max_epochs: int = 30, max_steps: Optional[int] = None,
            logger: bool = True, tb_port: Optional[int] = None,
            log_save_interval: int = 100, progress_bar_rate: int = 10,
            log_gpu_memory: Optional[str] = None, model_summary_mode: str = 'top', # 'full', 'top'
            root_dir: str = '/data/tmp'):
        super(EasyaiTrainer, self).__init__(max_epochs=max_epochs, max_steps=max_steps,
                logger=logger,
                log_save_interval=log_save_interval, progress_bar_refresh_rate=progress_bar_rate,
                log_gpu_memory=log_gpu_memory, weights_summary=model_summary_mode,
                default_root_dir=root_dir, gpus=[0])

        if tb_port:
            k12ai_set_notebook(cellw=95)
            k12ai_start_tensorboard(tb_port, root_dir, clear=True)
