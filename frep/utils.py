import xlrd
import cv2
import os
import io
import json
import requests
import time
import threading
from minio import Minio

import warnings
warnings.filterwarnings('ignore')

S3_PREFIX = 'https://frepai.s3.didiyunapi.com'
VOD_PATH = 'datasets/vod'

DEVICES = (
    ["00232ee8876d", "机器焊接", "SSAC-292217-AAFFA"],
    ["00856405d389", "机器切割", "SSAE-110460-AABAE"],
    ["00047dd87188", "双人翻边", "SSAC-292170-BAAEC"],
    ["002b359e3931", "木槌加固", "SSAC-292197-ECFAB"]
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


def oss_get_bypath(path, ignores=['outputs', 'counts']):
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


def oss_put_file(src_url, dst_path, ct='video/mp4'):
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
    elif VOD_PATH in video_url:
        label = video_url.split('/')[-2]

    return f'{VOD_PATH}/{label}'


def start_inference(
        context, btn, w_raceurl,
        w_task, w_msgkey, w_true, w_pred, w_acc, w_bar, w_out, w_mp4, w_sim):
    raceurl = w_raceurl.value
    # task = w_task.value
    msgkey = w_msgkey.value
    api_popmsg = f'{raceurl}/raceai/private/popmsg?key={msgkey}'
    api_inference = f'{raceurl}/raceai/framework/inference'
    reqdata = context.get_all_json()
    video_url = reqdata['cfg']['video']
    requests_get(url=api_popmsg)
    result = json.loads(requests.post(url=api_inference, json=reqdata).text)
    w_out.value = json.dumps(reqdata, indent=4)
    if 'errno' in result:
        if result['errno'] < 0:
            w_out.value = json.dumps(result, indent=4)
            return

    btn.disabled = True

    def _run_result(btn, w_true, w_pred, w_acc, w_bar, w_out, w_mp4, w_sim):
        cur_try = 0
        err_max = 60
        while cur_try < err_max:
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
                w_out.value = json.dumps(result, indent=4)
                options = []
                if 'stride_mp4' in result:
                    options.append(('stride_mp4', result['stride_mp4']))
                if 'target_mp4' in result:
                    options.append(('target_mp4', result['target_mp4']))
                w_mp4.options = options
                if 'vod' in video_url and 'sumcnt' in result:
                    w_pred.value = round(result['sumcnt'], 2)
                    context.logger(f'inference result: {w_pred.value}')
                    if w_true.value > 0:
                        w_acc.value = round(100 * (1 - abs(w_pred.value - w_true.value) / w_true.value), 2)
                if 'embs_sims' in result:
                    w_sim.value = result['embs_sims']
        btn.disabled = False
    threading.Thread(target=_run_result, kwargs={
        'btn': btn,
        'w_true': w_true,
        'w_pred': w_pred,
        'w_acc': w_acc,
        'w_bar': w_bar,
        'w_out': w_out,
        'w_mp4': w_mp4,
        'w_sim': w_sim,
    }).start()


def stop_inference(context, btn, start_button):
    start_button.disabled = False


def save_jsonconfig(context, btn, w_video, w_load):
    mp4_name = os.path.basename(w_video.value)
    sample_path = _parse_sample_video_path(w_video.value)
    path = f'{sample_path}/{mp4_name[:-4]}.json'
    context.logger(f'save_jsonconfig: {path}')
    data = context.get_all_kv(False)
    for wid in SAVE_IGNORE_WIDS:
        data.pop(wid, None)
    etag = oss_put_jsonconfig(path, data)
    if etag:
        w_load.disabled = False
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


def save_group_jsonconfig(context, btn_noused, w_video, w_load):
    sample_path = _parse_sample_video_path(w_video.value)
    path = f'{sample_path}/config.json'
    data = context.get_all_kv(False)
    for wid in SAVE_IGNORE_WIDS:
        data.pop(wid, None)
    data.pop('_cfg.accuracy')
    data.pop('_cfg.true_count')
    data.pop('_cfg.pred_count')
    context.logger(f'save_group_jsonconfig:{path}')
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


def show_video_frame(context, source, oldval, newval, btn_mp4conf, btn_grpconf, w_image, w_mp4, w_sim):
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
        conf = json.loads(response.content.decode('utf-8'))
    else:
        btn_mp4conf.disabled = True
        if 'vod' in path:
            context.get_widget_byid('_cfg.accuracy').value = 0.0
            context.get_widget_byid('_cfg.true_count').value = 0
            context.get_widget_byid('_cfg.pred_count').value = 0

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
    ts = oss_get_bypath(f'{os.path.dirname(sample_path)}/outputs/{mp4_name[:-4]}/', ignores=[])
    if len(ts) > 0:
        if len(ts) > 1 and ts[0][0].startswith('nb'):
            output_path = ts[1][1] # TODO
        else:
            output_path = ts[0][1]

        options = []
        if oss_path_exist(f'{output_path}/target-stride.mp4'):
            options.append(('stride_mp4', f'{S3_PREFIX}/{output_path}/target-stride.mp4'))
        if oss_path_exist(f'{output_path}/target.mp4'):
            options.append(('stride_mp4', f'{S3_PREFIX}/{output_path}/target.mp4'))
        if len(options) > 0:
            w_mp4.options = options
        if oss_path_exist(f'{output_path}/embs_sims.npy'):
            w_sim.value = f'{S3_PREFIX}/{output_path}/embs_sims.npy'


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

    if oss_put_file(video_url, f'{sample_path}/{mp4_name}'):
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
    if newval > 0:
        w_acc.value = round(100 * (1 - abs(w_pred.value - newval) / newval), 2)
        context.logger(f'w_acc: {w_acc.value}')


EVENTS = {
    'start_inference': start_inference,
    'stop_inference': stop_inference,
    'save_jsonconfig': save_jsonconfig,
    'load_jsonconfig': load_jsonconfig,
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
}
