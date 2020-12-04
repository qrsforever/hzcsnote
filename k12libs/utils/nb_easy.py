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
from functools import reduce
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

from abc import ABC, abstractmethod # noqa

from collections import OrderedDict
import numpy as np
import torch
import torch.nn as nn # noqa
import torchvision # noqa
from PIL import Image # noqa
from torch.nn.modules.module import _addindent

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True
# Access-Control-Allow-Origin
CORS(app, supports_credentials=True)

# Global
g_queue = None
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

## RACE

RACEURL = 'http://{}:{}'.format(netip, 9119) # RaceAI API
RACE_ROOT = '/raceai'
RACE_DATA = f'{RACE_ROOT}/data'


def _start_flask_service():
    try:
        requests.get('http://{}:{}/shutdown'.format(flask_host, flask_port))
    except Exception:
        pass

    def _run_flask(*args, **kwargs):
        try:
            app.run(*args, **kwargs, debug=False)
        except Exception:
            pass
    threading.Thread(target=_run_flask,
            kwargs={"host": flask_host, "port": flask_port}).start()

@app.route('/shutdown', methods=['GET'])
def _flask_shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/k12ai/notebook/message', methods=['POST', 'GET'])
def _flask_handle():
    try:
        reqjson = json.loads(request.get_data().decode())
        msgtype = reqjson['msgtype']
        if msgtype == 'protodata':
            tag = reqjson['tag']
            ctx = g_contexts.get(tag, None)
            if ctx:
                ctx.protodata = reqjson[msgtype]
                return json.dumps({'tags': 'context of %s %s' % (tag, list(g_contexts.keys()))})
            else:
                return json.dumps({'error': 'not found context of %s %s' % (tag, list(g_contexts.keys()))})
        elif msgtype == 'genpycode':
            net_def = reqjson['net_def']
            tag = reqjson['tag']
            ctx = g_contexts.get(tag, None)
            if ctx is None:
                return json.dumps({'error': 'not found context of %s %s' % (tag, list(g_contexts.keys()))})
            sys.path.append(k12ai_get_app_dir('cv'))
            from vulkan.builders.net_builder import NetBuilder
            net = NetBuilder(net_def).build_net()
            net.write_net('/tmp/net_def.py')
            sys.path.remove(k12ai_get_app_dir('cv'))
            with open('/tmp/net_def.py', 'r') as fr:
                response = {'pycode': str(fr.read())}
                return json.dumps(response)
        elif msgtype == 'facedet':
            host = reqjson['host']
            port = reqjson['port']
            api = f'http://{host}:{port}/colorai/face_detection'
            response = json.loads(requests.post(url=api, json=reqjson).text)
            if '100200' == response['code']:
                return json.dumps(response['content'])
            else:
                return json.dumps({'error': response['content']})
        elif msgtype == 'lpdet':
            host = reqjson['host']
            port = reqjson['port']
            api = f'http://{host}:{port}/colorai/licenseplate_detection'
            response = json.loads(requests.post(url=api, json=reqjson).text)
            if '100200' == response['code']:
                return json.dumps(response['content'])
            else:
                return json.dumps({'error': response['content']})
        elif msgtype == 'dogcat':
            host = reqjson['host']
            port = reqjson['port']
            api = f'http://{host}:{port}/colorai/dogcat_predict'
            response = json.loads(requests.post(url=api, json=reqjson).text)
            if '100200' == response['code']:
                return json.dumps(response['content'])
            else:
                return json.dumps({'error': response['content']})
        elif msgtype == 'garbage':
            host = reqjson['host']
            port = reqjson['port']
            api = f'http://{host}:{port}/colorai/garbage_predict'
            response = json.loads(requests.post(url=api, json=reqjson).text)
            if '100200' == response['code']:
                return json.dumps(response['content'])
            else:
                return json.dumps({'error': response['content']})
        else:
            return json.dumps({'error': 'unkown type'})
    except Exception as err:
        err = {'error': format(err)}
        return json.dumps(err)
    return 'ok'

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

def k12ai_start_html(uri, width=None, height=None, flask=False):
    token = '&' if '?' in uri else '?'
    if not uri.startswith('http'):
        uri = f'{W3URL}/{uri}'
    k12ai_set_notebook(cellw=95)
    if width is None:
        width = '100%'
    if height is None:
        height = 300
    if flask:
        uri += f'{token}flask=http://{netip}:{flask_port}/k12ai/notebook/message'
        _start_flask_service()
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

def k12ai_get_www_dir():
    return os.path.join(k12ai_get_top_dir(), 'k12libs', 'www')

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
        active_time = 0
        while True:
            try:
                tag, key, flag = g_queue.get(True, timeout=timeout)
                context = g_contexts.get(tag, None)
                active_time = time.time()
                if flag == 1:
                    with context.progress.output:
                        clear_output()
                        context.traindata = {
                                'tmpfile': os.path.join(k12ai_get_www_dir(), f'cache/metrics_{tag}.json'),
                                'metrics': []}
                    timeout = 1
                    total_count = 0
                    result = {}
                    continue
                elif flag == 2:
                    timeout = 50
                elif flag == 3:
                    context.progress.trainstart.disabled = False
                    context.progress.trainstop.disabled = True
                    context.progress.value = 100.0
                    context.progress.description = '100.0%'
                    timeout = 300
                    if len(context.traindata['metrics']) > 0:
                        with context.progress.output:
                            clear_output(wait=True)
                            with open(context.traindata['tmpfile'], 'w') as fw:
                                json.dump(context.traindata['metrics'], fw, ensure_ascii=False)
                            print(f'Download full metrics: {W3URL}/cache/metrics_{tag}.json')
                    continue
                elif flag == 9:
                    timeout = 1
                    continue
                else:
                    timeout = 3
            except Empty:
                timeout = min(1 + int((time.time() - active_time) / 2), 50)
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
                result['data'] = {}
                result['error'] = {}
                result['metrics'] = {}
                # error
                data = k12ai_get_data(key, 'error', num=1, rm=True)
                if data:
                    result['error'] = data[0]['value']
                    code = result['error']['data']['code']
                    # 100003: finish 100004: stop
                    if code == 100003 or code == 100004 or code > 100100:
                        g_queue.put((context.tag, key, 3))

                # metrics
                if context.progress.phase == 'train':
                    data = k12ai_get_data(key, 'metrics', num=100, rm=True)
                    result['data'] = data
                    if data:
                        result['metrics'] = data[-1]['value']
                        if context.framework == 'k12ml':
                            context.progress.value = 1.0
                        else:
                            for obj in result['metrics']['data']:
                                if obj['type'] == 'scalar':
                                    if 'progress' in obj['data']['title']:
                                        progress = obj['data']['payload']['y'][0]['value']
                                        context.progress.value = progress
                else: # context.progress.phase == 'evaluate':
                    data = k12ai_get_data(key, 'metrics', num=100, rm=True)
                    if data:
                        result['metrics'] = data[-1]['value']
                        context.progress.value = result['metrics']['data']['progress']
            except Exception:
                pass

            if 'error' in result and len(result['error']) > 0:
                context._output(result['error'])
            if 'metrics' in result and len(result['metrics']) > 0:
                with context.progress.output:
                    clear_output(wait=True)
                    k12ai_print(result['metrics'])
                    context.traindata['metrics'].extend([x['value'] for x in result['data']])

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
    context.tag = str(id(context))[:6]
    # context.tag = hashlib.md5(tag.encode()).hexdigest()[0:6]
    context.uuid = context.tag
    context.usercache = f'{K12AI_USERS_ROOT}/{context.user}/{context.uuid}'
    context.tb_logdir = f'{K12AI_TBLOG_ROOT}/{context.user}/{context.uuid}'
    context.dataset_dir = f'{K12AI_DATASETS_ROOT}/{context.framework[3:]}/{context.dataset}'
    context.dataset_url = f'{DSURL}'

    if 'custom' in context.network and not context.model_templ:
        context.model_templ = 'simple'

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
        _start_flask_service()

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
    g_queue.put((context.tag, key, 3))


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
    k12ai_set_notebook(cellw=95)
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

def k12ai_model_summary(model, input_size: tuple = None):

    if input_size and len(input_size) >= 3:
        if len(input_size) == 4:
            batch_size = input_size[0]
            input_size = input_size[1:]
        else:
            batch_size = -1

        def summary_string(model, input_size, batch_size=-1, device=torch.device('cuda:0'), dtypes=None):
            if dtypes is None:
                dtypes = [torch.FloatTensor]*len(input_size)

            summary_str = ''

            def register_hook(module):
                def hook(module, input, output):
                    class_name = str(module.__class__).split(".")[-1].split("'")[0]
                    module_idx = len(summary)

                    m_key = "%s-%i" % (class_name, module_idx + 1)
                    summary[m_key] = OrderedDict()
                    if isinstance(input[0], list):
                        print(len(input[0]))
                    summary[m_key]["input_shape"] = list(input[0].size())
                    summary[m_key]["input_shape"][0] = batch_size
                    if isinstance(output, (list, tuple)):
                        summary[m_key]["output_shape"] = [
                            [-1] + list(o.size())[1:] for o in output
                        ]
                    else:
                        summary[m_key]["output_shape"] = list(output.size())
                        summary[m_key]["output_shape"][0] = batch_size

                    params = 0
                    if hasattr(module, "weight") and hasattr(module.weight, "size"):
                        params += torch.prod(torch.LongTensor(list(module.weight.size())))
                        summary[m_key]["trainable"] = module.weight.requires_grad
                    if hasattr(module, "bias") and hasattr(module.bias, "size"):
                        params += torch.prod(torch.LongTensor(list(module.bias.size())))
                    summary[m_key]["nb_params"] = params

                # if (
                #     not isinstance(module, nn.Sequential)
                #     and not isinstance(module, nn.ModuleList)
                # ):
                if not any(module.children()):
                    hooks.append(module.register_forward_hook(hook))

            # multiple inputs to the network
            if isinstance(input_size, tuple):
                input_size = [input_size]

            # batch_size of 2 for batchnorm
            x = [torch.rand(2, *in_size).type(dtype).to(device=device)
                 for in_size, dtype in zip(input_size, dtypes)]

            # create properties
            summary = OrderedDict()
            hooks = []

            # register hook
            model.apply(register_hook)

            # make a forward pass
            # print(x.shape)
            model(*x)

            # remove these hooks
            for h in hooks:
                h.remove()

            summary_str += "----------------------------------------------------------------" + "\n"
            line_new = "{:>20}  {:>25} {:>15}".format(
                "Layer (type)", "Output Shape", "Param #")
            summary_str += line_new + "\n"
            summary_str += "================================================================" + "\n"
            total_params = 0
            total_output = 0
            trainable_params = 0
            for layer in summary:
                # input_shape, output_shape, trainable, nb_params
                line_new = "{:>20}  {:>25} {:>15}".format(
                    layer,
                    str(summary[layer]["output_shape"]),
                    "{0:,}".format(summary[layer]["nb_params"]),
                )
                total_params += summary[layer]["nb_params"]

                total_output += np.prod(summary[layer]["output_shape"])
                if "trainable" in summary[layer]:
                    if summary[layer]["trainable"]:
                        trainable_params += summary[layer]["nb_params"]
                summary_str += line_new + "\n"

            # assume 4 bytes/number (float on cuda).
            total_input_size = abs(np.prod(sum(input_size, ())) * batch_size * 4. / (1024 ** 2.))
            total_output_size = abs(2. * total_output * 4. / (1024 ** 2.))  # x2 for gradients
            total_params_size = abs(total_params * 4. / (1024 ** 2.))
            total_size = total_params_size + total_output_size + total_input_size

            summary_str += "================================================================" + "\n"
            summary_str += "Total params: {0:,}".format(total_params) + "\n"
            summary_str += "Trainable params: {0:,}".format(trainable_params) + "\n"
            summary_str += "Non-trainable params: {0:,}".format(total_params - trainable_params) + "\n"
            summary_str += "----------------------------------------------------------------" + "\n"
            summary_str += "Input size (MB): %0.2f" % total_input_size + "\n"
            summary_str += "Forward/backward pass size (MB): %0.2f" % total_output_size + "\n"
            summary_str += "Params size (MB): %0.2f" % total_params_size + "\n"
            summary_str += "Estimated Total Size (MB): %0.2f" % total_size + "\n"
            summary_str += "----------------------------------------------------------------" + "\n"
            # return summary
            return summary_str, (total_params, trainable_params)

        result, _ = summary_string(model, input_size, batch_size, next(model.parameters()).device)
        print(result)

    def repr(model):
        # We treat the extra repr like the sub-module, one item per line
        extra_lines = []
        extra_repr = model.extra_repr()
        # empty string will be split into list ['']
        if extra_repr:
            extra_lines = extra_repr.split('\n')
        child_lines = []
        total_params = 0
        for key, module in model._modules.items():
            if module is None:
                continue
            mod_str, num_params = repr(module)
            mod_str = _addindent(mod_str, 2)
            child_lines.append('(' + key + '): ' + mod_str)
            total_params += num_params
        lines = extra_lines + child_lines

        for name, p in model._parameters.items():
            if p is not None:
                total_params += reduce(lambda x, y: x * y, p.shape)

        main_str = model._get_name() + '('
        if lines:
            # simple one-liner info, which most builtin Modules will use
            if len(extra_lines) == 1 and not child_lines:
                main_str += extra_lines[0]
            else:
                main_str += '\n  ' + '\n  '.join(lines) + '\n'

        main_str += ')'
        main_str += ', {:,} params'.format(total_params)
        return main_str, total_params

    string, count = repr(model)

    # Building hierarchical output
    _pad = int(max(max(len(_) for _ in string.split('\n')) - 20, 0) / 2)
    lines = list()
    lines.append('=' * _pad + ' Hierarchical Summary ' + '=' * _pad + '\n')
    lines.append(string)
    lines.append('\n\n' + '=' * (_pad * 2 + 22) + '\n')

    str_summary = '\n'.join(lines)
    print(str_summary)
