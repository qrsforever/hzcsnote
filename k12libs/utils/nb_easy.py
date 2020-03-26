#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file nb_global_env.py
# @brief
# @author QRS
# @version 1.0
# @date 2019-12-06 12:16:50

import os
import base64
import hashlib
import requests
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

from IPython.display import clear_output, display, HTML
from .nb_widget import K12WidgetGenerator
import ipywidgets as widgets

import signal
from tensorboard import notebook as tbnotebook
from tensorboard import manager as tbmanager

import matplotlib.pyplot as plt # noqa
# from matplotlib.ticker import MultipleLocator

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

NBURL = 'http://{}:{}'.format(host, 8118) # Jupyter
AIURL = 'http://{}:{}'.format(host, 8119) # K12AI API
SSURL = 'http://{}:{}'.format(host, 8500) # Consul
TBURL = 'http://{}:{}'.format(host, 6006) # Tensorboard
DSURL = 'http://{}:{}'.format(host, 9090) # Dataset

K12AI_HOST_ADDR = host
K12AI_WLAN_ADDR = consul_addr

## DIR
K12AI_DATASETS_ROOT = '/data/datasets'
K12AI_USERS_ROOT = '/data/users'
K12AI_NBDATA_ROOT = '/data/nb_data'


def k12ai_set_notebook(cellw=None):
    if cellw:
        display(HTML('<style>.container { width:%d%% !important; }</style>' % cellw))


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

# def k12ai_get_status_data(datakey, num=1):
#     return k12ai_get_data(datakey, 'status', num)

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


g_queue = None
g_process = None
g_contexts = {}
g_axes = None
g_figure = None

# g_xlocator = MultipleLocator(20)

def _start_work_process(context):
    global g_queue, g_process, g_contexts, g_axes, g_figure

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
                    # g_axes[0].cla()
                    # g_axes[1].cla()
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
                context.progress.description = str(context.progress.value)
            else:
                context.progress.description = 'Progress:'

            try:
                # error
                result['error'] = {}
                data = k12ai_get_data(key, 'error', num=1)
                if data:
                    result['error'] = data[0]['value']
                    code = result['error']['data']['code']
                    if code != 100001 and code != 100002:
                        g_queue.put((context.tag, key, 3))

                # metrics
                if context.progress.phase == 'train':
                    data = k12ai_get_data(key, 'metrics', num=1, rm=True)
                    if data:
                        result['metrics'] = data[0]['value']
                        if context.framework == 'k12ml':
                            # with context.progress.output:
                            #     clear_output()
                            #     k12ai_print(data)
                            context.progress.value = 1.0
                        else:
                            contents = data[0]['value']['data']
                            context.progress.value = contents['training_progress']
                        #     iters = contents['training_iters']

                        #     with context.progress.output:
                        #         clear_output(wait=True)
                        #         if contents.get('training_loss', None):
                        #             g_axes[0].set_xticks(())
                        #             g_axes[0].set_ylabel('Loss')
                        #             g_axes[0].scatter([iters], [contents['training_loss']], color='k')
                        #         if contents.get('training_score', None):
                        #             g_axes[1].set_xticks(())
                        #             g_axes[1].set_ylabel('Score')
                        #             g_axes[1].scatter([iters], [contents['training_score']], color='k')
                        #         display(g_figure)
                        #         plt.show()
                        #         g_queue.put((context.tag, key, 9))
                elif context.progress.phase == 'evaluate':
                    data = k12ai_get_data(key, 'metrics', num=10, rm=True)
                    if data:
                        result['metrics'] = data[-1]['value']
                        context.progress.value = result['metrics']['data']['evaluate_progress']
                        # with context.progress.output:
                        #     clear_output()
                        #     k12ai_print(data)
            except Exception:
                pass

            if len(result) > 0:
                if 'error' in result:
                    context._output(result['error'])
                if 'metrics' in result:
                    with context.progress.output:
                        clear_output(wait=True)
                        k12ai_print(result['metrics'])

    # plt.ioff()
    # if g_axes is None:
    #     fig, axes = plt.subplots(1, 2, figsize=(12, 8))

    #     for i in (0, 1):
    #         axes[i].spines['right'].set_color('none')
    #         axes[i].spines['top'].set_color('none')
    #         axes[i].locator_params(nbins = 6)
    #         axes[i].set_xlabel('Iters')

    #     plt.tight_layout(pad=3, h_pad=3.5, w_pad=3.5)
    #     g_axes = axes
    #     g_figure = fig

    if not g_process or not g_process.is_alive():
        # g_process = multiprocessing.Process(target=_queue_work, args=())
        g_process = threading.Thread(target=_queue_work, args=())
        g_process.start()
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
    context.tb_logdir = f'{context.usercache}/tblogs'
    context.dataset_dir = f'{K12AI_DATASETS_ROOT}/{context.framework[3:]}/{context.dataset}'

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

    context.parse_schema(json.loads(response['data']), tb_url=tb_url)

    if context.framework == 'k12cv':
        if context.network.split('_')[0] == 'custom':
            if context.task == 'cls' and context.dataset == 'mnist':
                from k12libs.templates.cls.custom_mnist import NETWORK_MNIST_DEF
                context.wid_widget_map['network.net_def'].value = NETWORK_MNIST_DEF
            elif context.task == 'det':
                from k12libs.templates.det.custom_ssd import NETWORK_BACKBONE_DEF
                context.wid_widget_map['network.net_def'].value = NETWORK_BACKBONE_DEF


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
        framework=None, task=None, network=None, dataset=None):
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
            network = 'base_model' if framework == 'k12cv' else 'basic_classifier'
        _init_project_schema(context, {
            'project.framework': framework,
            'project.task': task,
            'project.network': network,
            'project.dataset': dataset
        })
    display(context.page)
    return context

def k12ai_get_config(framework, task, network, dataset):
    context = K12WidgetGenerator()
    response = json.loads(k12ai_post_request(
        uri='k12ai/framework/schema',
        data={
            'service_name': framework,
            'service_task': task,
            'dataset_name': dataset,
            'network_type': network
        }))
    context.parse_schema(json.loads(response['data']))
    return context.get_all_kv()


def k12ai_train_execute(framework='k12cv', task='cls', network='base_model',
         backbone='vgg11', dataset='Boats', batchsize=32, inputsize=32, iter_num=1, run_num=1):
    config = k12ai_get_config(framework, task, network, dataset)
    if framework == 'k12cv':
        config['train.batch_size'] = batchsize
        config['train.data_transformer.input_size'] = [inputsize, inputsize]
        config['solver.lr.metric'] = 'iters'
        config['solver.max_iters'] = iter_num
        if backbone:
            network = backbone
            config['network.backbone'] = backbone
    user = '15801310416'
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

        data['op'] = 'train.start'
        data['service_params'] = config
        k12ai_post_request(uri='k12ai/framework/execute', data=data)

        keys.append(f'framework/{user}/{uuid}/train')
    return keys
