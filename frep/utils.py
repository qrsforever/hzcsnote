import xlrd
import cv2
import os
import io
import json
import requests
import time
import threading
from minio import Minio
from multiprocessing import Event

import warnings
warnings.filterwarnings('ignore')

S3_PREFIX = 'https://frepai.s3.didiyunapi.com'
VOD_PATH = 'datasets/vod'

g_exited = Event()


DEVICES = (
    ["00232ee8876d", "机器焊接", "SSAC-292217-AAFFA"],
    ["00856405d389", "机器切割", "SSAE-110460-AABAE"],
    ["00047dd87188", "双人翻边", "SSAC-292170-BAAEC"],
    ["002b359e3931", "木槌加固", "SSAC-292197-ECFAB"],
    ["00baf49e6f65", "小型冲床", "SSAE-110478-AAFDC"],
    ["00fb00f23a41", "激光印章", "SSAC-233524-DFDCC"],
    ["0031059d1d11", "坐姿切割", "SSAC-292202-FBDEB"],
    ["00a57548b004", "新版1", "SSAE-110468-AFCBD"],
    ["005cfa60d733", "新版2", "SSAE-110438-CEAAC"],
    ["00d8c273f993", "新版3", "SSAE-110447-DAEED"],
    ["00bd4ac291c5", "新版4", "SSAE-110434-ECCFD"],
)


def requests_get(url, verify=False):
    try:
        url = url.replace('frepai.s3.', 'frepai.s3-internal.')
        return requests.get(url, verify=verify)
    except Exception:
        pass
    return None


def get_jsonconfig(url, verify=False):
    try:
        url = url.replace('frepai.s3.', 'frepai.s3-internal.')
        response = requests.get(url, verify=verify)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
    except Exception:
        pass
    return None


oss_client = Minio(
    endpoint=os.environ.get('MINIO_SERVER_URL'),
    access_key=os.environ.get('MINIO_ACCESS_KEY'),
    secret_key=os.environ.get('MINIO_SECRET_KEY'),
    secure=True)


def oss_path_exist(path):
    try:
        oss_client.stat_object('frepai', path)
    except Exception:
        return False
    return True


def oss_get_bypath(path, ignores=['outputs', 'counts', 'unkown']):
    objs = oss_client.list_objects('frepai', path, recursive=False)
    options = []
    for o in objs:
        object_path = o.object_name
        if object_path[-1] == '/':
            object_path = object_path[:-1]
        object_name = os.path.basename(object_path)
        if object_name in ignores:
            continue
        options.append((object_name, object_path))
    if len(options) == 0:
        options = [('NONE', 'NONE')]
    return sorted(options, key=lambda item: item[0], reverse=True)


def oss_get_jsonconfig(path):
    if path.startswith('http'):
        path = '/'.join(path[8:].split('/')[1:])
    data = oss_client.get_object('frepai', path)
    if data:
        return json.loads(data.data.decode('utf-8'))
    return {}


def oss_put_jsonconfig(path, data):
    if isinstance(data, (dict, list)):
        data = json.dumps(data, ensure_ascii=False, indent=4)
    with io.BytesIO(data.encode()) as bio:
        size = bio.seek(0, 2)
        bio.seek(0, 0)
        etag = oss_client.put_object('frepai', path, bio, size, content_type='text/json')
        if not isinstance(etag, str):
            etag = etag.etag
        return etag

def oss_put_file(src_path, dst_path, ct='binary/octet-stream'):
    oss_client.fput_object('frepai', dst_path, src_path, content_type=ct)
    return True

def oss_put_bytes(_bytes, dst_path, ct='binary/octet-stream'):
    with io.BytesIO(_bytes) as bio:
        oss_client.put_object(
            'frepai', dst_path,
            bio, len(_bytes), content_type=ct)
    return True

def oss_put_urlfile(src_url, dst_path, ct='video/mp4'):
    for _ in range(2):
        try:
            result = requests_get(src_url.replace('s3', 's3-internal'))
            with io.BytesIO(result.content) as bio:
                oss_client.put_object(
                    'frepai', dst_path,
                    bio, len(result.content), content_type=ct)
            return True
        except Exception:
            time.sleep(1)
    return False


def oss_del_files(dst_path, recursive=False):
    try:
        if recursive:
            objs = oss_client.list_objects('frepai', dst_path, recursive=True)
            for o in objs:
                oss_client.remove_object('frepai', o.object_name)
        else:
            oss_client.remove_object('frepai', dst_path)
        return True
    except Exception:
        pass
    return False


def oss_get_video_list(prefix):
    objs = oss_client.list_objects('frepai', f'{prefix}/counts/', recursive=False)
    crecs = {}
    for o in objs:
        if o.object_name[-4:] != 'json':
            continue
        segs = os.path.basename(o.object_name)[:-5].split('_')
        crecs[segs[0] + '.mp4'] = segs[1]

    objs = oss_client.list_objects('frepai', f'{prefix}/videos/', recursive=False)
    options = []
    for o in objs:
        if o.object_name[-3:] != 'mp4':
            continue
        oname = os.path.basename(o.object_name)
        hour = int(oname[8:10])
        if hour > 7 and hour < 19:
            key = oname[8:]
            if oname in crecs:
                key += f'        {crecs[oname]}'
            options.append((key, f'{S3_PREFIX}/{o.object_name}'))
    if len(options) == 0:
        options = [('NONE', 'NONE')]
    return sorted(options, key=lambda item: item[0], reverse=True)


def oss_get_video_samples(prefix):
    if prefix[-1] != '/':
        prefix += '/'
    objs = oss_client.list_objects('frepai', prefix, recursive=False)
    options = []
    for o in objs:
        if o.object_name[-3:] != 'mp4':
            continue
        options.append((os.path.basename(o.object_name), f'{S3_PREFIX}/{o.object_name}'))
    if len(options) == 0:
        options = [('NONE', 'NONE')]
    return sorted(options, key=lambda item: item[0], reverse=True)


def parse_xls_report():
    for file in os.listdir('report'):
        if not file.endswith('xls'):
            continue
        file = f'report/{file}'
        data = xlrd.open_workbook(file)
        table = data.sheets()[0]
        for i in range(table.nrows):
            rowdata = table.row_values(i)
            if '摄像头' not in rowdata:
                continue
            taskt_col = rowdata.index('任务类型')
            count_col = rowdata.index('审核次数')
            video_col = rowdata.index('视频源地址')
            taskt_info = table.col_values(taskt_col)[i + 1:]
            count_info = table.col_values(count_col)[i + 1:]
            video_info = table.col_values(video_col)[i + 1:]
            for task, count, url in zip(taskt_info, count_info, video_info):
                if task and count and url:
                    if isinstance(count, str) and '+' in count:
                        count = eval(count)
                    filename = os.path.basename(url).replace('.mp4', f'_{int(count)}.mp4')
                    result = requests_get(url)
                    oss_client.put_object(
                        'frepai', f'datasets/ladder/{task}/{filename}',
                        io.BytesIO(result.content), len(result.content), content_type='video/mp4')
            break
        os.remove(file)


def draw_scale(image, d=50):
    h, w, _ = image.shape
    cx, cy = int(w / 2), int(h / 2)
    hor, ver = d / w, d / h
    hor_seq = [(i * d, i * hor) for i in range(1, round(cx / d))]
    ver_seq = [(i * d, i * ver) for i in range(1, round(cy / d))]

    # Center
    image = cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1)

    circ_color = (0, 0, 0)
    font_color = (200, 250, 200)

    # Horizontal
    for shift, scale in hor_seq:
        # Left
        cv2.circle(image, ((cx - shift), cy), 3, circ_color, -1)
        cv2.putText(image, '%.2f' % (0.5 - scale), (cx - shift - 15, cy + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
        # Right
        cv2.circle(image, ((cx + shift), cy), 3, circ_color, -1)
        cv2.putText(image, '%.2f' % (0.5 + scale), (cx + shift - 15, cy - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)

    # Vertical
    for shift, scale in ver_seq:
        # Up
        cv2.circle(image, (cx, (cy - shift)), 3, circ_color, -1)
        cv2.putText(image, '%.2f' % (0.5 - scale), (cx - 40, cy - shift + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
        # Down
        cv2.circle(image, (cx, (cy + shift)), 3, circ_color, -1)
        cv2.putText(image, '%.2f' % (0.5 + scale), (cx + 4, cy + shift + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)

    return image

SAVE_IGNORE_WIDS = ['cfg.pigeon.msgkey', 'cfg.video', '_cfg.race_url']


def _parse_sample_video_path(video_url):
    label = 'unkown'
    if 'com/live' in video_url:
        mac = video_url[8:].split('/')[2]
        for dev in DEVICES:
            if dev[0] == mac:
                label = dev[1]
    elif 'datasets/factory' in video_url:
        mac = video_url[8:].split('/')[3]
        for dev in DEVICES:
            if dev[0] == mac:
                label = dev[1]
    elif VOD_PATH in video_url:
        label = video_url.split('/')[-2]

    return f'{VOD_PATH}/{label}'


def start_pcaks_test(
        context, btn, w_raceurl, w_task, w_msgkey,
        w_samples, w_single_start, w_bar, w_out):
    context.logger('start_pcaks_test start')

    raceurl = w_raceurl.value
    msgkey = w_msgkey.value
    api_popmsg = f'{raceurl}/frepai/private/popmsg?key={msgkey}'
    api_inference = f'{raceurl}/frepai/framework/inference'

    w_single_start.disabled = True
    w_bar.value = 0.0

    reqdata = {
        'task': w_task.value,
        'cfg': {
            'pigeon': {'msgkey': msgkey},
            'pcaks': []
        }
    }
    sample_path = None
    for i, (label, url) in enumerate(w_samples.options, 1):
        mp4_name = os.path.basename(url)
        if sample_path is None:
            sample_path = _parse_sample_video_path(url)
            grp_config_file = f'{S3_PREFIX}/{sample_path}/config.json'
            response = requests_get(grp_config_file)
            if response.status_code == 200:
                gconf = json.loads(response.content.decode('utf-8'))
                scaler = gconf.get('_cfg.pcaks.scaler', 'Normalizer')
                nc = gconf.get('_cfg.pcaks.nc', 100)
                reqdata['cfg']['scaler'] = scaler
                reqdata['cfg']['n_components'] = nc
                reqdata['cfg']['pigeon']['out_path'] = f'{S3_PREFIX}/{sample_path}/pcaks_{scaler}_{nc}.pkl'
            else:
                w_out.value = f'Not found group config file {grp_config_file}'
                w_single_start.disabled = False
                w_bar.value = 100.0
                return
        path = f'{sample_path}/{mp4_name[:-4]}.json'
        response = requests_get(f'{S3_PREFIX}/{path}')
        if response.status_code == 200:
            conf = json.loads(response.content.decode('utf-8'))
            if conf and '_cfg.sims_slice' in conf and len(conf['_cfg.sims_slice']) > 0:
                reqdata['cfg']['pcaks'].append({
                    'ef_url': f'{S3_PREFIX}/{os.path.dirname(sample_path)}/outputs/{mp4_name[:-4]}/repnet_tf/embs_feat.npy',  # noqa
                    'slices': conf['_cfg.sims_slice'],
                })

    def _run_result(btn, params, api_popmsg, api_inference, w_bar, w_out):
        requests_get(url=api_popmsg)
        result = json.loads(requests.post(url=api_inference, json=params).text)
        if 'errno' in result:
            if result['errno'] < 0:
                btn.disabled = False
                w_bar.value = 100.0
                w_out.value = json.dumps(result, indent=4)
                return
        cur_try = 0
        err_max = 60
        w_bar.description = 'Progress(pcaks):'
        while not g_exited.is_set() and cur_try < err_max:
            result = json.loads(requests_get(url=api_popmsg).text)
            if len(result) == 0:
                time.sleep(1)
                cur_try += 1
                continue
            cur_try = 0
            result = result[-1]
            if result['errno'] == 0:
                btn.disabled = False
                w_bar.value = 100.0
                w_out.value = json.dumps(result, indent=4, ensure_ascii=False)
                break

    g_exited.clear()
    threading.Thread(target=_run_result, kwargs={
        'btn': w_single_start,
        'params': reqdata,
        'api_popmsg': api_popmsg,
        'api_inference': api_inference,
        'w_bar': w_bar,
        'w_out': w_out,
    }).start()


def group_sample_update(context, btn, grpbtn):
    if hasattr(grpbtn, 'samples') and grpbtn.samples is not None:
        sample_path = None
        for label, conf in grpbtn.samples.items():
            mp4_name = os.path.basename(conf['cfg.video'])
            if sample_path is None:
                sample_path = _parse_sample_video_path(conf['cfg.video'])
            path = f'{sample_path}/{mp4_name[:-4]}.json'
            for key in SAVE_IGNORE_WIDS:
                conf.pop(key, None)
            etag = oss_put_jsonconfig(path, conf)
            context.logger(f'{label}[{path}] oss upload {etag} ok!')


def group_start_inference(
        context, btn, w_raceurl, w_task, w_msgkey,
        w_samples, w_single_start, w_bar, w_out):
    N = len(w_samples.options)
    if N == 0:
        w_out.value = 'Error: 0 Files'
        w_single_start.disabled = False
        return

    context.logger(f'group_start_inference count: {N}')
    raceurl = w_raceurl.value
    msgkey = w_msgkey.value
    api_popmsg = f'{raceurl}/frepai/private/popmsg?key={msgkey}'
    api_inference = f'{raceurl}/frepai/framework/inference'

    w_single_start.disabled = True

    w_bar.value = 0.0

    btn.samples = {}
    options = []
    sample_path = None
    for i, (label, url) in enumerate(w_samples.options, 1):
        t, p, a = 0, 0, 0
        mp4_name = os.path.basename(url)
        if sample_path is None:
            sample_path = _parse_sample_video_path(url)
        path = f'{sample_path}/{mp4_name[:-4]}.json'
        response = requests_get(f'{S3_PREFIX}/{path}')
        if response.status_code == 200:
            conf = json.loads(response.content.decode('utf-8'))
            if conf:
                t, p, a = conf['_cfg.true_count'], conf['_cfg.pred_count'], conf['_cfg.accuracy'] # noqa
        options.append((url, label, t, p, a))

    grp_config_file = f'{S3_PREFIX}/{sample_path}/config.json'
    response = requests_get(grp_config_file)
    if response.status_code == 200:
        btn.train_params_kvs = json.loads(response.content.decode('utf-8'))
        btn.train_params_kvs['cfg.save_video'] = False
        btn.train_params_kvs['cfg.pigeon'] = {'msgkey': msgkey}
        btn.train_params_kvs['cfg.best_stride_video'] = False
    else:
        w_out.value = f'{grp_config_file} file is not found!'
        w_single_start.disabled = False
        return


    def _run_result(btn, single_btn, train_params, api_popmsg, api_inference, options, w_bar, w_out):
        w_bar.value = 0
        w_out.value = '{:^24s}|{:^28s}|{:^10s}|{:^10s}|\t{}\n'.format(
                'ID', 'ACC_N vs ACC_O', 'True', 'Pred', 'SIGN')
        N = len(options)
        seg_prg = 100 / N
        rec_sign_counts = [0, 0, 0]

        for i, (url, label, true_value, old_count, old_acc) in enumerate(options):
            if g_exited.is_set():
                break
            train_params['cfg']['video'] = url
            requests_get(url=api_popmsg)
            result = json.loads(requests.post(url=api_inference, json=train_params).text)
            if 'errno' in result:
                if result['errno'] < 0:
                    continue
            cur_try = 0
            err_max = 60
            w_bar.description = 'Progress({:03d}/{:03d}):'.format(i+1, N)
            while not g_exited.is_set() and cur_try < err_max:
                result = json.loads(requests_get(url=api_popmsg).text)
                if len(result) == 0:
                    time.sleep(1)
                    cur_try += 1
                    continue
                cur_try = 0
                result = result[-1]
                if result['errno'] == 0:
                    progress = result['progress']
                    if progress < 100.0:
                        w_bar.value = seg_prg * (i + progress / 100)
                        continue
                    w_bar.value = (i + 1) * seg_prg
                    acc_value = 0
                    if 'sumcnt' in result:
                        pred_value = round(result['sumcnt'], 2)
                        if true_value > 0 and pred_value > 0:
                            if pred_value > true_value:
                                acc_value = round(100 * true_value / pred_value, 2)
                            else:
                                acc_value = round(100 * pred_value / true_value, 2)
                    if acc_value > old_acc:
                        rec_sign_counts[0] += 1
                        sign = '👍'
                    elif acc_value < old_acc:
                        rec_sign_counts[1] += 1
                        sign = '👎'
                    else:
                        rec_sign_counts[2] += 1
                        sign = '✊'
                    w_out.value += '\n{:^20s}\t|{:<6.2f} {:>6.2f}|\t{:>6.2f}\t{:>6.2f}\t{}'.format(
                            label, acc_value, old_acc, true_value, pred_value, sign) # noqa
                    btn.samples[label] = btn.train_params_kvs.copy()
                    btn.samples[label]['_cfg.true_count'] = true_value
                    btn.samples[label]['_cfg.pred_count'] = pred_value
                    btn.samples[label]['_cfg.accuracy'] = acc_value
                    btn.samples[label]['cfg.video'] = url
                    break
            else:
                w_out.value += f'\n{label} quit or timeout: {cur_try}'
        w_out.value += '\n\nResult:\n\t 👍: {:>3d} \t{:>4.1f}%\n\t 👎: {:>3d} \t{:>4.1f}%\n\t ✊: {:>3d} \t{:>4.1f}%'.format(
                rec_sign_counts[0], (100 * rec_sign_counts[0])/len(options),
                rec_sign_counts[1], (100 * rec_sign_counts[1])/len(options),
                rec_sign_counts[2], (100 * rec_sign_counts[2])/len(options))
        single_btn.disabled = False
        w_bar.description = 'Progress:'

    g_exited.clear()
    threading.Thread(target=_run_result, kwargs={
        'btn': btn,
        'single_btn': w_single_start,
        'train_params': context.get_all_json(btn.train_params_kvs),
        'api_popmsg': api_popmsg,
        'api_inference': api_inference,
        'options': options,
        'w_bar': w_bar,
        'w_out': w_out,
    }).start()


def start_inference(
        context, btn, w_raceurl,
        w_task, w_msgkey, w_true, w_pred, w_acc, w_bar, w_out, w_mp4):
    raceurl = w_raceurl.value
    # task = w_task.value
    msgkey = w_msgkey.value
    api_popmsg = f'{raceurl}/frepai/private/popmsg?key={msgkey}'
    api_inference = f'{raceurl}/frepai/framework/inference'
    reqdata = context.get_all_json()
    video_url = reqdata['cfg']['video']
    requests_get(url=api_popmsg)
    result = json.loads(requests.post(url=api_inference, json=reqdata).text)
    w_out.value = json.dumps(reqdata, indent=4, ensure_ascii=False)
    if 'errno' in result:
        if result['errno'] < 0:
            w_out.value = json.dumps(result, indent=4)
            return

    btn.disabled = True

    def _run_result(btn, w_true, w_pred, w_acc, w_bar, w_out, w_mp4):
        cur_try = 0
        err_max = 60
        w_bar.description = 'Progress(001/001):'
        ts_token = int(time.time())
        while not g_exited.is_set() and cur_try < err_max:
            result = json.loads(requests_get(url=api_popmsg).text)
            if len(result) == 0:
                time.sleep(1)
                cur_try += 1
                continue
            result = result[-1]
            cur_try = 0
            if result['errno'] != 0:
                btn.disabled = False
                w_out.value = json.dumps(result, indent=4)
                w_bar.value = 100.0
                break
            w_bar.value = int(result['progress'])
            if w_bar.value == 100.0:
                btn.disabled = False
                w_out.value = json.dumps(result, indent=4, ensure_ascii=False)
                options = []
                if 'stride_mp4' in result:
                    options.append(('stride_mp4', result['stride_mp4'] + f'?{ts_token}'))
                if 'target_mp4' in result:
                    options.append(('target_mp4', result['target_mp4'] + f'?{ts_token}'))
                w_mp4.options = options
                if 'vod' in video_url and 'sumcnt' in result:
                    w_pred.value = round(result['sumcnt'], 2)
                    context.logger(f'inference result: {w_pred.value}')
                    if w_true.value > 0 and w_pred.value > 0:
                        if w_pred.value > w_true.value:
                            w_acc.value = round(100 * w_true.value / w_pred.value, 2)
                        else:
                            w_acc.value = round(100 * w_pred.value / w_true.value, 2)
        btn.disabled = False


    g_exited.clear()
    threading.Thread(target=_run_result, kwargs={
        'btn': btn,
        'w_true': w_true,
        'w_pred': w_pred,
        'w_acc': w_acc,
        'w_bar': w_bar,
        'w_out': w_out,
        'w_mp4': w_mp4,
    }).start()


def stop_inference(context, btn, start_button, grp_start_button):
    start_button.disabled = False
    grp_start_button.disabled = False
    g_exited.set()


def save_jsonconfig(context, btn, w_video, w_load, w_del):
    mp4_name = os.path.basename(w_video.value)
    sample_path = _parse_sample_video_path(w_video.value)
    path = f'{sample_path}/{mp4_name[:-4]}.json'
    context.logger(f'save_jsonconfig: {S3_PREFIX}/{path}')
    data = context.get_all_kv(False)
    for wid in SAVE_IGNORE_WIDS + ['_cfg.pcaks.scaler', '_cfg.pcaks.nc']:
        data.pop(wid, None)
    etag = oss_put_jsonconfig(path, data)
    if etag:
        w_load.disabled = False
        w_del.disabled = False
    else:
        context.logger('save error')


def load_jsonconfig(context, btn, w_video):
    mp4_name = os.path.basename(w_video.value)
    sample_path = _parse_sample_video_path(w_video.value)
    path = f'{sample_path}/{mp4_name[:-4]}.json'
    context.logger(f'load_jsonconfig: {path}')
    response = requests_get(f'{S3_PREFIX}/{path}', verify=False)
    if response.status_code == 200:
        context.set_widget_values(json.loads(response.content.decode('utf-8')))
    else:
        context.logger('load error')


def delete_jsonconfig(context, btn, w_video, w_load):
    mp4_name = os.path.basename(w_video.value)
    sample_path = _parse_sample_video_path(w_video.value)
    path = f'{sample_path}/{mp4_name[:-4]}.json'
    context.logger(f'delete_jsonconfig: {path}')
    if oss_del_files(path):
        w_load.disabled = True
        btn.disabled = True
    else:
        context.logger('delete error')


def save_group_jsonconfig(context, btn_noused, w_video, w_load):
    sample_path = _parse_sample_video_path(w_video.value)
    path = f'{sample_path}/config.json'
    data = context.get_all_kv(False)
    for wid in SAVE_IGNORE_WIDS + ['_cfg.sims_slice', '_cfg.accuracy', '_cfg.true_count', '_cfg.pred_count']:
        data.pop(wid, None)
    context.logger(f'save_group_jsonconfig: {S3_PREFIX}/{path}')
    etag = oss_put_jsonconfig(path, data)
    if etag:
        w_load.disabled = False
    else:
        context.logger('save group error')


def load_group_jsonconfig(context, btn_noused, w_video):
    sample_path = _parse_sample_video_path(w_video.value)
    path = f'{sample_path}/config.json'
    response = requests_get(f'{S3_PREFIX}/{path}')
    if response.status_code == 200:
        context.set_widget_values(json.loads(response.content.decode('utf-8')))
    else:
        context.logger('load group error')


def frep_schema_init():
    device_list = [(name, mac) for mac, name, _ in DEVICES]
    date_list = oss_get_bypath(f'live/{device_list[0][1]}/')[:7]
    video_list = oss_get_video_list(date_list[0][1])
    task_list = oss_get_bypath(f'datasets/vod/')
    if len(task_list) != len(device_list):
        for dev in device_list:
            if dev[0] not in task_list:
                oss_put_jsonconfig(f'datasets/vod/{dev[0]}/info.json', [])
    sample_list = oss_get_video_samples(task_list[0][1])
    return device_list, date_list, video_list, task_list, sample_list


def get_date_list(context, source, oldval, newval, target):
    context.logger(f'get_date_list:{oldval} {newval}')
    target.options = oss_get_bypath(f'live/{newval}/')[:7]
    target.value = target.options[0][1]


def get_video_list(context, source, oldval, newval, target):
    target.options = oss_get_video_list(newval)
    target.value = target.options[0][1]
    context.logger(f'get_video_list:{oldval} {newval} {target.value}')


def get_sample_list(context, source, oldval, newval, target):
    target.options = oss_get_video_samples(newval)
    target.value = target.options[0][1]
    context.logger(f'get_sample_list:{oldval} {newval} {target.value}')


def focus_center_changed(context, source, oldval, newval, target):
    context.logger(f'focus_center_changed:{oldval} to {newval}')
    newval = newval if newval.strip()[0] == '[' else '[' + newval + ']'
    points = json.loads(newval)
    w, h = 640, 352 # TODO
    if len(points) == 2:
        points = [0.5, 0.5, points[0], points[1]]
    if len(points) == 4:
        if 0 < points[0] < 1.0 and 0 < points[1] < 1.0:
            cx, cy = points[0], points[1]
        else:
            cx, cy = round(points[0] / w, 3), round(points[1] / h, 3)

        if 0 < points[2] < 1.0 and 0 < points[3] < 1.0:
            dx, dy = points[2], points[3]
        else:
            dx, dy = round(points[2] / w, 3), round(points[3] / h, 3)

        fx1, fy1 = cx - dx, cy - dy
        fx2, fy2 = cx + dx, cy + dy
        target.value = '[%.3f,%.3f,%.3f,%.3f]' % (fx1, fy1, fx2, fy2)


def focus_box_changed(context, source, oldval, newval, target):
    context.logger(f'focus_box_changed:{oldval} to {newval}')
    newval = newval if newval.strip()[0] == '[' else '[' + newval + ']'
    points = json.loads(newval)
    if target.value and len(points) == 4:
        img = target.image.copy() # cv2.imdecode(np.frombuffer(target.value, np.uint8), cv2.IMREAD_COLOR)
        h, w, _ = img.shape
        if isinstance(points[0], float):
            fx1, fy1 = int(points[0] * w), int(points[1] * h)
            fx2, fy2 = int(points[2] * w), int(points[3] * h)
        else:
            fx1, fy1 = points[0], points[1]
            fx2, fy2 = points[2], points[3]
        cv2.rectangle(img, (fx1, fy1), (fx2, fy2), (0, 255, 0), 2)
        target.value = io.BytesIO(cv2.imencode('.png', img)[1]).getvalue()


def black_box_changed(context, source, oldval, newval, target):
    context.logger(f'black_box_changed:{oldval} to {newval}')
    newval = newval if newval.strip()[0] == '[' else '[' + newval + ']'
    points = json.loads(newval)
    if target.value and len(points) == 4:
        img = target.image.copy()
        h, w, _ = img.shape
        if isinstance(points[0], float):
            fx1, fy1 = int(points[0] * w), int(points[1] * h)
            fx2, fy2 = int(points[2] * w), int(points[3] * h)
        else:
            fx1, fy1 = points[0], points[1]
            fx2, fy2 = points[2], points[3]
        cv2.rectangle(img, (fx1, fy1), (fx2, fy2), (0, 0, 0), 2)
        target.value = io.BytesIO(cv2.imencode('.png', img)[1]).getvalue()


def show_video_frame(context, source, oldval, newval, btn_mp4conf, btn_delconf, btn_grpconf, w_image, w_mp4):
    context.logger(f'show_video_frame:{oldval} to {newval}')
    if newval == 'NONE':
        return

    cap = cv2.VideoCapture(newval)
    if cap.isOpened():
        _, frame_bgr = cap.read()
        frame_bgr = draw_scale(frame_bgr)
        w_image.value = io.BytesIO(cv2.imencode('.png', frame_bgr)[1]).getvalue()
        w_image.image = frame_bgr

    mp4_name = os.path.basename(newval)
    sample_path = _parse_sample_video_path(newval)
    conf = None

    # mp4 btn
    path = f'{sample_path}/{mp4_name[:-4]}.json'
    response = requests_get(f'{S3_PREFIX}/{path}')
    context.logger(f'show_video_frame: request {S3_PREFIX}/{path} [{response.status_code}]')
    if response.status_code == 200:
        btn_mp4conf.disabled = False
        btn_delconf.disabled = False
        conf = json.loads(response.content.decode('utf-8'))
    else:
        btn_mp4conf.disabled = True
        btn_delconf.disabled = True
        if 'vod' in newval:
            context.get_widget_byid('_cfg.accuracy').value = 0.0
            context.get_widget_byid('_cfg.true_count').value = 0
            context.get_widget_byid('_cfg.pred_count').value = 0
        else:
            config_url = newval.replace('videos', 'outputs').replace('.mp4', '/repnet_tf/config.json')
            context.logger(f'show_video_frame: raw config {config_url}')

    # group btn
    path = f'{sample_path}/config.json'
    response = requests_get(f'{S3_PREFIX}/{path}')
    context.logger(f'show_video_frame: request {S3_PREFIX}/{path} [{response.status_code}]')
    if response.status_code == 200:
        btn_grpconf.disabled = False
        if conf is None:
            conf = json.loads(response.content.decode('utf-8'))
    else:
        btn_grpconf.disabled = True

    # set configure
    if conf:
        context.logger(f'{conf}')
        if '_cfg.sims_slice' not in conf:
            conf['_cfg.sims_slice'] = ''
        changed_items = context.set_widget_values(conf)
        context.logger(f'{changed_items}')
        # TODO
        if 'cfg.focus_box' in conf and 'cfg.focus_box' not in changed_items:
            focus_box_changed(
                context, context.get_widget_byid('cfg.focus_box'),
                '[]', json.dumps(conf['cfg.focus_box']), w_image
            )
        if 'cfg.black_box' in conf and 'cfg.black_box' not in changed_items:
            focus_box_changed(
                context, context.get_widget_byid('cfg.black_box'),
                '[]', json.dumps(conf['cfg.black_box']), w_image
            )

    # output files
    ts_token = int(time.time())
    output_path = f'{os.path.dirname(sample_path)}/outputs/{mp4_name[:-4]}/repnet_tf'
    options = []
    if oss_path_exist(f'{output_path}/target-stride.mp4'):
        options.append(('stride_mp4', f'{S3_PREFIX}/{output_path}/target-stride.mp4?{ts_token}'))
    if oss_path_exist(f'{output_path}/target.mp4'):
        options.append(('stride_mp4', f'{S3_PREFIX}/{output_path}/target.mp4?{ts_token}'))
    w_mp4.options = options


def check_video_sample(context, source, oldval, newval, btn_upload, btn_remove):
    context.logger(f'check_video_sample:{oldval} to {newval}')
    video_url = newval
    if video_url == 'NONE':
        btn_upload.disabled = True
        btn_remove.disabled = True
        return
    mp4_name = os.path.basename(video_url)
    sample_path = _parse_sample_video_path(video_url)
    if oss_path_exist(f'{sample_path}/{mp4_name}'):
        btn_upload.disabled = True
        btn_remove.disabled = False
    else:
        btn_upload.disabled = False
        btn_remove.disabled = True


def upload_sample(context, btn_upload, btn_remove, wid_tsklist, wid_smplist, wid_result, wid_video):
    context.logger(f'upload_sample: {wid_video.value}')
    wid_result.value = ''
    video_url = wid_video.value
    mp4_name = os.path.basename(video_url)
    sample_path = _parse_sample_video_path(video_url)

    if oss_put_urlfile(video_url, f'{sample_path}/{mp4_name}'):
        btn_upload.disabled = True
        btn_remove.disabled = False
        wid_result.value = 'SUCCESS'
        if wid_tsklist.value in sample_path:
            wid_smplist.options = oss_get_video_samples(sample_path)
            wid_smplist.value = f'{S3_PREFIX}/{sample_path}/{mp4_name}'
    else:
        wid_result.value = 'FAILD'
        context.logger(f'put {sample_path}/{mp4_name} err')


def remove_sample(context, btn_remove, btn_upload, wid_tsklist, wid_smplist, wid_result, wid_video):
    context.logger(f'remove_sample: {wid_video.value}')
    wid_result.value = ''
    video_url = wid_video.value
    mp4_name = os.path.basename(video_url)
    sample_path = _parse_sample_video_path(video_url)

    if oss_del_files(f'{sample_path}/{mp4_name[:-4]}', recursive=True):
        wid_result.value = 'SUCCESS'
        btn_upload.disabled = False
        btn_remove.disabled = True
        if 'vod' in video_url:
            wid_smplist.options = oss_get_video_samples(sample_path)
            wid_smplist.value = wid_smplist.options[0][1]
    else:
        wid_result.value = 'FAIL'
        context.logger(f'del {sample_path}/{mp4_name} err')

def update_rep_count(context, source, oldval, newval, w_sample, w_pred, w_acc):
    context.logger(f'update_rep_count: {newval}, {w_sample.value}')
    if newval > 0 and w_pred.value > 0:
        if w_pred.value > newval:
            w_acc.value = round(100 * newval / w_pred.value, 2)
        else:
            w_acc.value = round(100 * w_pred.value / newval, 2)
        context.logger(f'w_acc: {w_acc.value}')


def on_tabpage_envent(context, source, oldval, newval, w_navi, w_grp_start):
    if w_navi.value != 1:
        w_grp_start.disabled = True
    else:
        w_grp_start.disabled = False


EVENTS = {
    'start_pcaks_test': start_pcaks_test,
    'group_start_inference': group_start_inference,
    'group_sample_update': group_sample_update,
    'start_inference': start_inference,
    'stop_inference': stop_inference,
    'save_jsonconfig': save_jsonconfig,
    'load_jsonconfig': load_jsonconfig,
    'delete_jsonconfig': delete_jsonconfig,
    'save_group_jsonconfig': save_group_jsonconfig,
    'load_group_jsonconfig': load_group_jsonconfig,
    'get_date_list': get_date_list,
    'get_video_list': get_video_list,
    'get_sample_list': get_sample_list,
    'show_video_frame': show_video_frame,
    'focus_center_changed': focus_center_changed,
    'focus_box_changed': focus_box_changed,
    'black_box_changed': black_box_changed,
    'check_video_sample': check_video_sample,
    'upload_sample': upload_sample,
    'remove_sample': remove_sample,
    'update_rep_count': update_rep_count,

    'on_tabpage_envent': on_tabpage_envent,
}
