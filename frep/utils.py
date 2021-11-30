import xlrd
import cv2
import os
import io
import json
import requests
import time
import threading
from minio import Minio

S3_PREFIX = 'https://frepai.s3.didiyunapi.com/'


oss_client = Minio(
    endpoint=os.environ.get('MINIO_SERVER_URL'),
    access_key=os.environ.get('MINIO_ACCESS_KEY'),
    secret_key=os.environ.get('MINIO_SECRET_KEY'),
    secure=True)


def oss_get_bypath(path):
    objs = oss_client.list_objects('frepai', path, recursive=False)
    options = []
    for o in objs:
        object_path = o.object_name
        if object_path[-1] == '/':
            object_path = object_path[:-1]
        options.append((os.path.basename(object_path), object_path))
    if len(options) == 0:
        options = [('NONE', 'NONE')]
    return options


def oss_put_jsonfile(path, data):
    if isinstance(data, dict):
        data = json.dumps(data, ensure_ascii=False, indent=4)
    data = io.BytesIO(data.encode())
    size = data.seek(0, 2)
    data.seek(0, 0)
    etag = oss_client.put_object('frepai', path, data, size, content_type='text/json')
    if not isinstance(etag, str):
        etag = etag.etag
    return etag


def oss_get_video_list(prefix):
    objs = oss_client.list_objects('frepai', f'{prefix}/videos/', recursive=False)
    options = []
    for o in objs:
        if o.object_name[-3:] != 'mp4':
            continue
        options.append((os.path.basename(o.object_name)[8:], S3_PREFIX + o.object_name))
    if len(options) == 0:
        options = [('NONE', 'NONE')]
    return options


def oss_get_video_samples(prefix):
    if prefix[-1] != '/':
        prefix += '/'
    objs = oss_client.list_objects('frepai', prefix, recursive=False)
    options = []
    for o in objs:
        if o.object_name[-3:] != 'mp4':
            continue
        options.append((os.path.basename(o.object_name), S3_PREFIX + o.object_name))
    if len(options) == 0:
        options = [('NONE', 'NONE')]
    return options


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
                    result = requests.get(url.replace('s3', 's3-internal'))
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


def start_inference(context, btn, w_raceurl, w_task, w_msgkey, w_acc, w_bar, w_out, w_mp4, w_skewing):
    raceurl = w_raceurl.value
    task = w_task.value
    msgkey = w_msgkey.value
    api_popmsg = f'{raceurl}/raceai/private/popmsg?key={msgkey}'
    api_inference = f'{raceurl}/raceai/framework/inference'
    reqdata = context.get_all_json()
    video_url = reqdata['cfg']['video']
    requests.get(url=api_popmsg)
    result = json.loads(requests.post(url=api_inference, json=reqdata).text)
    w_out.value = json.dumps(reqdata, indent=4)
    if 'errno' in result:
        if result['errno'] < 0:
            w_out.value = json.dumps(result, indent=4)
            return

    btn.disabled = True

    def _run_result(btn, w_acc, w_bar, w_out, w_mp4, w_skewing):
        cur_try = 0
        err_max = 60
        while cur_try < err_max:
            result = json.loads(requests.get(url=api_popmsg).text)
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
                if 'ladder' in video_url and 'sumcnt' in result:
                    count = int(os.path.basename(video_url).split('_')[1][:-4])
                    context.logger(f'inference result: {count}/{result["sumcnt"]}')
                    if count > 0:
                        w_acc.value = round(100 * (1 - abs(result['sumcnt'] - count) / count), 2)
                    if 'detinfo' in result:
                        if result['detinfo']['focus_skewing']:
                            w_skewing.value = w_skewing.options[1][1]
                        else:
                            w_skewing.value = w_skewing.options[0][1]
        btn.disabled = False
    threading.Thread(target=_run_result, kwargs={
        'btn': btn,
        'w_acc': w_acc,
        'w_bar': w_bar,
        'w_out': w_out,
        'w_mp4': w_mp4,
        'w_skewing': w_skewing,
    }).start()


def stop_inference(context, btn, start_button):
    start_button.disabled = False


def save_jsonconfig(context, btn, w_video, w_load):
    path = w_video.value[len(S3_PREFIX):-4] + '.json'
    context.logger(f'save_jsonconfig: {path}')
    data = w_video.context.get_all_kv(False)
    for wid in SAVE_IGNORE_WIDS:
        data.pop(wid, None)
    etag = oss_put_jsonfile(path, data)
    if etag:
        w_load.disabled = False
    context.logger(f'save_jsonconfig:{path}')


def load_jsonconfig(context, btn, w_video):
    path = w_video.value.replace('.mp4', '.json')
    context.logger(f'load_jsonconfig: {path}')
    response = requests.get(path)
    if response.status_code == 200:
        context.set_widget_values(json.loads(response.content.decode('utf-8')))


def save_group_jsonconfig(context, btn, w_video, w_load):
    path = w_video.value
    if 'live' in path:
        path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
    else:
        path = os.path.dirname(path)
    path += '/config.json'
    data = context.get_all_kv(False)
    for wid in SAVE_IGNORE_WIDS:
        data.pop(wid, None)
    etag = oss_put_jsonfile(path[len(S3_PREFIX):], data)
    if etag:
        w_load.disabled = False
    context.logger(f'save_group_jsonconfig:{path}')


def load_group_jsonconfig(context, btn, w_video):
    path = w_video.value
    if 'live' in path:
        path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
    else:
        path = os.path.dirname(path)
    path += '/config.json'
    response = requests.get(path)
    if response.status_code == 200:
        context.set_widget_values(json.loads(response.content.decode('utf-8')))


def get_date_list(context, source, oldval, newval, target):
    context.logger(f'get_date_list:{oldval} {newval}')
    target.options = oss_get_bypath(f'live/{newval}/')[-7:]
    target.value = target.options[-1][1]


def get_video_list(context, source, oldval, newval, target):
    context.logger(f'get_video_list:{oldval} {newval}')
    target.options = oss_get_video_list(newval)
    target.value = target.options[int(len(target.options) / 2)][1]


def get_sample_list(context, source, oldval, newval, target):
    context.logger(f'get_sample_list:{oldval} {newval}')
    target.options = oss_get_video_samples(newval)
    target.value = target.options[int(len(target.options) / 2)][1]


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


def show_video_frame(context, source, oldval, newval, btn_mp4conf, btn_grpconf, w_image):
    context.logger(f'show_video_frame:{oldval} to {newval}')
    if newval == 'NONE':
        return

    cap = cv2.VideoCapture(newval)
    # fps = round(cap.get(cv2.CAP_PROP_FPS))
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # th = int(0.08 * height)
    if cap.isOpened():
        _, frame_bgr = cap.read()
        frame_bgr = draw_scale(frame_bgr)
        w_image.value = io.BytesIO(cv2.imencode('.png', frame_bgr)[1]).getvalue()
        w_image.image = frame_bgr

    path = newval
    # group btn
    if 'live' in path:
        path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
    else:
        path = os.path.dirname(path)
    path += '/config.json'
    response = requests.get(path)
    if response.status_code == 200:
        btn_grpconf.disabled = False
    else:
        btn_grpconf.disabled = True

    # mp4 btn
    skew_wdg = context.get_widget_byid('_cfg.skewing')
    path = newval.replace('.mp4', '.json')
    response = requests.get(path)
    if response.status_code == 200:
        btn_mp4conf.disabled = False
        conf = json.loads(response.content.decode('utf-8'))
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
        if '_cfg.skewing' in conf:
            skew_wdg.value = conf['_cfg.skewing']
        else:
            skew_wdg.value = skew_wdg.options[0][1]
    else:
        context.get_widget_byid('_cfg.accuracy').value = 0.0
        skew_wdg.value = skew_wdg.options[0][1]
        btn_mp4conf.disabled = True


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
}
