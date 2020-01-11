#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file nb_global_env.py
# @brief
# @author QRS
# @version 1.0
# @date 2019-12-06 12:16:50

import os
import base64
import requests
import json
import _jsonnet
import consul
import time
import socket
import threading
import multiprocessing
from multiprocessing.queues import Empty

from IPython.display import clear_output
from IPython.display import display
from .nb_widget import K12WidgetGenerator
import ipywidgets as widgets

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

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

consul_addr = get_net_ip()
consul_port = 8500

NBURL = 'http://{}:{}'.format(host, 8118)
AIURL = 'http://{}:{}'.format(host, 8119)
SSURL = 'http://{}:{}'.format(host, 8500)

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

def k12ai_get_status_data(datakey, num=1):
    return k12ai_get_data(datakey, 'status', num)

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
        "op":"%s",
        "user": "%s",
        "service_name": "k12cv",
        "service_uuid": "%s",
        "service_params": %s
    }''' % (op, user, uuid, params))
    api = 'http://%s:%d/%s' % (host, port, uri)
    key = 'framework/%s/%s/%s' % (user, uuid, op)
    return {'req': data,
            'res': json.loads(requests.post(url=api, json=data).text),
            'key': key}

def k12ai_post_nlp_request(uri, op, user, uuid, params=None):
    if not params:
        params = '{}'
    if isinstance(params, dict):
        params = json.dumps(params)
    data = json.loads('''{
        "op":"%s",
        "user": "%s",
        "service_name": "k12nlp",
        "service_uuid": "%s",
        "service_params": %s
    }''' % (op, user, uuid, params))
    api = 'http://%s:%d/%s' % (host, port, uri)
    key = 'framework/%s/%s/%s' % (user, uuid, op)
    return {'req': data,
            'res': json.loads(requests.post(url=api, json=data).text),
            'key': key}

def k12ai_post_platform_request(uri, op, user, uuid, params=None, isasync=False):
    if not params:
        params = '{}'
    if isinstance(params, dict):
        params = json.dumps(params)
    data = json.loads('''{
        "op":"%s",
        "user": "%s",
        "service_name": "k12platform",
        "service_uuid": "%s",
        "service_params": %s,
        "async": %s
    }''' % (op, user, uuid, params, 'true' if isasync else 'false'))
    api = 'http://%s:%d/%s' % (host, port, uri)
    key = 'platform/%s/%s/%s' % (user, uuid, op)
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


g_queue = None
g_process = None
g_contexts = {}
g_drawits = None
g_figure = None

g_xlocator = MultipleLocator(20)

def _start_work_process(context):
    global g_queue, g_process, g_contexts, g_drawits, g_figure

    if not g_queue:
        g_queue = multiprocessing.Queue()

    def _queue_work():
        context = None
        key = None
        timeout = 3
        while True:
            try:
                tag, key, timeout = g_queue.get(True, timeout=timeout)
                context = g_contexts.get(tag, None)
            except Empty:
                pass
            except AttributeError:
                pass

            if not context or not key:
                continue

            result = {}
            data = k12ai_get_data(key, 'status', num=1)
            if data:
                result['status'] = data[0]['value']
            data = k12ai_get_data(key, 'error', num=1)
            if data:
                result['error'] = data[0]['value']
                if result['error']['contents']['code'] != 100000:
                    context.train_progress.trainstart.disabled = False
                    context.train_progress.trainstop.disabled = True
                    timeout = 300
            data = k12ai_get_data(key, 'metrics', num=1, rm=True)
            if data:
                result['metrics'] = data[0]['value']
                contents = data[0]['value']['contents']
                context.train_progress.value = contents['training_epochs']
                iters = contents['training_iters']
                with context.train_progress.drawit:
                    clear_output(wait=True)
                    g_drawits[0, 0].scatter([iters], [contents['training_loss']])
                    g_drawits[0, 1].scatter([iters], [contents['training_speed']])
                    display(g_figure)
                    plt.show()

            if len(result) > 0:
                context._output(result)

    if not g_process or not g_process.is_alive():
        # g_process = multiprocessing.Process(target=_queue_work, args=())
        g_process = threading.Thread(target=_queue_work, args=())
        g_process.start()
        time.sleep(1.5)

    if g_drawits is None:
        plt.ioff()
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        for i in [0, 1]:
            for j in [0, 1]:
                axes[i, j].spines['right'].set_color('none')
                axes[i, j].spines['top'].set_color('none')
                # axes[i, j].grid(True)
                axes[i, j].set_xlabel('Iters')
                axes[i, j].set_xticks([])
                axes[i, j].set_xticklabels([])

        axes[0, 0].set_ylabel('Loss')
        axes[0, 1].set_ylabel('Speed')
        axes[1, 0].set_ylabel('LR')
        axes[1, 1].set_ylabel('ACC')

        axes[0, 0].locator_params("x", nbins = 6)
        axes[0, 0].locator_params("y", nbins = 6)
        axes[0, 0].xaxis.set_major_locator(g_xlocator)
        axes[0, 1].locator_params("x", nbins = 6)
        axes[0, 1].locator_params("y", nbins = 6)
        axes[0, 1].xaxis.set_major_locator(g_xlocator)
        plt.tight_layout(pad=3, h_pad=3.5, w_pad=3.5)
        g_drawits = axes
        g_figure = fig


def _init_project_schema(context, params):
    context._output('----------Generate Project Schema (take a monment: 5s)--------------')
    context._output(params, 0)

    context.user = params.get('project.user', None)
    context.uuid = params.get('project.uuid', None)
    context.framework = params.get('project.framework', None)
    context.task = params.get('project.task', None)
    context.dataset = params.get('project.dataset', None)
    context.tag = '%s_%s_%s' % (context.user, context.uuid, context.dataset)
    g_contexts[context.tag] = context

    if context.framework == 'k12cv':
        schema = os.path.join(k12ai_get_top_dir(), 'cv/app', 'templates', 'schema/k12ai_cv.jsonnet')
    elif context.framework == 'k12nlp':
        schema = os.path.join(k12ai_get_top_dir(), 'nlp/app', 'templates', 'schema/k12ai_nlp.jsonnet')
    else:
        raise()

    context.parse_schema(json.loads(_jsonnet.evaluate_file(schema,
        ext_vars={
            'task': context.task,
            'dataset_name': context.dataset})))

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
        wdg.progress.running = -1
        wdg.progress.value = 0

    wdg.progress.trainstart.disabled = True
    wdg.progress.trainstop.disabled = False

    if not hasattr(context, 'user'):
        context._output('train.start error, no context.user')
        return

    context._output('------------train.start--------------')
    op = 'train.start'
    response = json.loads(k12ai_post_request(
            uri='k12ai/framework/train',
            data= {
                'op': op,
                'user': context.user,
                'service_name': context.framework,
                'service_uuid': context.uuid,
                'service_params': context.get_all_kv()
                }))
    if response['code'] != 100000:
        context._output(response)
        return
    key = 'framework/%s/%s/%s' % (context.user, context.uuid, op)
    k12ai_del_data(key)
    _start_work_process(context)
    g_queue.put((context.tag, key, 3))

def _on_project_trainstop(wdg):
    if not hasattr(wdg, 'progress'):
        return
    wdg.progress.running = 0
    wdg.progress.trainstart.disabled = False
    wdg.progress.trainstop.disabled = True
    context = wdg.progress.context
    if not hasattr(context, 'user'):
        context._output('train.start error, no context.user')
        return
    op = 'train.stop'
    response = json.loads(k12ai_post_request(
            uri='k12ai/framework/train',
            data= {
                'op': op,
                'user': context.user,
                'service_name': context.framework,
                'service_uuid': context.uuid,
                }))
    if response['code'] != 100000:
        context._output(response)
        return
    key = 'framework/%s/%s/%s' % (context.user, context.uuid, op)
    k12ai_del_data(key)
    g_queue.put((context.tag, key, 600))

def _on_project_traininit(context, wdg_start, wdg_stop, wdg_progress, wdg_drawit):
    wdg_start.on_click(_on_project_trainstart)
    wdg_stop.on_click(_on_project_trainstop)

    wdg_start.progress = wdg_progress
    wdg_stop.progress = wdg_progress
    wdg_drawit.progress = wdg_progress

    wdg_progress.trainstart = wdg_start
    wdg_progress.trainstop = wdg_stop
    wdg_progress.drawit = wdg_drawit
    wdg_progress.context = context
    context.train_progress = wdg_progress

    response = json.loads(k12ai_post_request(
            uri='k12ai/platform/stats',
            data= {
                'op': 'query',
                'user': context.user,
                'service_name': 'k12platform',
                'service_uuid': context.uuid,
                'service_params': {'services': True},
                'async': False}))
    if response['code'] != 100000:
        context._output(response)
        return
    if len(response['message']['services']) == 1:
        wdg_start.disabled = True
        wdg_stop.disabled = False
        _start_work_process(context)
        key = 'framework/%s/%s/train.start' % (context.user, context.uuid)
        g_queue.put((context.tag, key, 3))
    else:
        wdg_start.disabled = False
        wdg_stop.disabled = True

def k12ai_run_project(lan='en', debug=True, framework=None):
    if framework is None:
        events = {
                'project.confirm': _on_project_confirm,
                'project.train.init': _on_project_traininit,
                }
        pro_schema = os.path.join(k12ai_get_top_dir(), 'k12libs/templates', 'projects.jsonnet')
        context = K12WidgetGenerator(lan, debug, events=events)
        context.parse_schema(json.loads(_jsonnet.evaluate_file(pro_schema)))
    else:
        events = {
                'project.train.init': _on_project_traininit,
                }
        context = K12WidgetGenerator(lan, debug, events=events)
        _init_project_schema(context, {
            'project.user': '16601548608',
            'project.uuid': '666666',
            'project.framework': framework,
            'project.task': 'cls' if framework == 'k12cv' else 'sa',
            'project.dataset': 'cifar10' if framework == 'k12cv' else 'sst',
            })
    display(context.page)
    return context
