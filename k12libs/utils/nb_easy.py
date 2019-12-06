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
import consul
import time
import socket

def get_host_ip():
    ip=''
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_net_ip():
    result = os.popen('curl -s http://txt.go.sohu.com/ip/soip| grep -P -o -i "(\d+\.\d+.\d+.\d+)"', 'r')
    if result:
        return result.read().strip('\n')
    return None

host = get_host_ip()
port = 8119

consul_addr = get_net_ip()
consul_port = 8500

def _print_json(text):
    if isinstance(text, str):
        print(json.dumps(json.loads(text), indent=4))
    else:
        print(json.dumps(text, indent=4))

def k12ai_print(text):
    if not text:
        return
    return _print_json(text)

def k12ai_post_request(uri, data):
    api = 'http://%s:%d/%s' % (host, port, uri)
    if isinstance(data, str):
        return _print_json(requests.post(url=api, json=json.loads(data)).text)
    if isinstance(data, dict):
        return _print_json(requests.post(url=api, json=data).text)
    return None

def k12ai_get_data(key, subkey=None, num=1, waitcnt=1, http=False):
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
            return out
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

def k12ai_get_error_data(datakey, num):
    return k12ai_get_data('%s/error' % datakey, num)

def k12ai_get_metrics_data(datakey, num):
    return k12ai_get_data('%s/metrics' % datakey, num)

def k12ai_post_cv_request(uri, op, user, uuid, params=None):
    if not params:
        params = '{}'
    data = '''{
        "op":"%s",
        "user": "%s",
        "service_name": "k12cv",
        "service_uuid": "%s",
        "service_params": %s
    }''' % (op, user, uuid, json.dumps(params))
    api = 'http://%s:%d/%s' % (host, port, uri)
    key = 'framework/%s/%s/%s' % (user, uuid, op)
    return requests.post(url=api, json=json.loads(data)).text, key

def k12ai_post_nlp_request(uri, op, user, uuid, params=None):
    if not params:
        params = '{}'
    data = '''{
        "op":"%s",
        "user": "%s",
        "service_name": "k12nlp",
        "service_uuid": "%s",
        "service_params": %s
    }''' % (op, user, uuid, json.dumps(params))
    api = 'http://%s:%d/%s' % (host, port, uri)
    key = 'framework/%s/%s/%s' % (user, uuid, op)
    return requests.post(url=api, json=json.loads(data)).text, key

def k12ai_json_load(path):
    if not os.path.exists(path):
        raise RuntimeError('not found file: %s' % path)
    str = ''
    with open(path, 'r') as f:
        str = json.load(f)
    return str
