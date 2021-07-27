import xlrd
import cv2
import os
import io
import json
import threading
from minio import Minio

oss_client = Minio(
    endpoint=os.environ.get('MINIO_SERVER_URL'),
    access_key=os.environ.get('MINIO_ACCESS_KEY'),
    secret_key=os.environ.get('MINIO_SECRET_KEY'),
    secure=True)

def oss_get_bypath(path):
    objs = oss_client.list_objects('frepai', path, recursive=False)
    options = []
    for o in objs:
        object_path = o.object_name[:-1]
        options.append((os.path.basename(object_path), object_path))
    if len(options) == 0:
        options = [('NONE', 'NONE')]
    return options

def oss_get_video_list(prefix):
    objs = oss_client.list_objects('frepai', f'{prefix}/videos/', recursive=False)
    options = []
    for o in objs:
        options.append((os.path.basename(o.object_name)[8:], 'https://frepai.s3.didiyunapi.com/' + o.object_name))
    if len(options) == 0:
        options = [('NONE', 'NONE')]
    return options

def oss_get_video_samples(prefix):
    if prefix[-1] != '/':
        prefix += '/'
    objs = oss_client.list_objects('frepai', prefix, recursive=False)
    options = []
    for o in objs:
        options.append((os.path.basename(o.object_name), 'https://frepai.s3.didiyunapi.com/' + o.object_name))
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
            video_col = rowdata.index('源视频地址')
            taskt_info = table.col_values(taskt_col)[i+1:]
            count_info = table.col_values(count_col)[i+1:]
            video_info = table.col_values(video_col)[i+1:]
            for task, count, url in zip(taskt_info, count_info, video_info):
                if task and count and url:
                    filename = os.path.basename(url).replace('.mp4', f'_{int(count)}.mp4')
                    result = requests.get(url.replace('s3', 's3-internal'))
                    oss_client.put_object(
                        'frepai', f'datasets/ladder/{task}/{filename}',
                        io.BytesIO(result.content), len(result.content), content_type='video/mp4')
            break
        os.remove(file)

def draw_scale(image, d=50):
    h, w, _ = image.shape 
    cx, cy = int(w /2), int(h / 2)
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

def get_date_list(source, oldval, newval, target):
    target.options = oss_get_bypath(f'live/{newval}/')[-7:]
    target.value = target.options[-1][1]
    
def get_video_list(source, oldval, newval, target):
    target.options = oss_get_video_list(newval)
    target.value = target.options[int(len(target.options) / 2)][1]
    
def get_sample_list(source, oldval, newval, target):
    target.options = oss_get_video_samples(newval)
    target.value = target.options[int(len(target.options) / 2)][1]
    
def show_video_frame(source, oldval, newval, target):
    cap = cv2.VideoCapture(newval)
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    th = int(0.08 * height)
    if cap.isOpened():
        _, frame_bgr = cap.read()
        frame_bgr = draw_scale(frame_bgr)
        target.value = io.BytesIO(cv2.imencode('.png', frame_bgr)[1]).getvalue()
        target.image = frame_bgr 
        
def focus_box_changed(source, oldval, newval, target):
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
        cv2.rectangle(img, (fx1, fy1), (fx2, fy2), (0, 255, 0), 2)
        target.value = io.BytesIO(cv2.imencode('.png', img)[1]).getvalue()

def black_box_changed(source, oldval, newval, target):
    points = json.loads(newval)
    if target.value and len(points) == 4:
        img = target.image
        h, w, _ = img.shape
        if isinstance(points[0], float):
            fx1, fy1 = int(points[0] * w), int(points[1] * h)
            fx2, fy2 = int(points[2] * w), int(points[3] * h)
        else:
            fx1, fy1 = points[0], points[1]
            fx2, fy2 = points[2], points[3]
        cv2.rectangle(img, (fx1, fy1), (fx2, fy2), (0, 0, 0), 2)
        target.value = io.BytesIO(cv2.imencode('.png', img)[1]).getvalue()
        
def center_rate_changed(source, oldval, newval, target):
    points = json.loads(newval)
    if target.value and len(points) == 2:
        img = target.image.copy()
        h, w, _ = img.shape
        if isinstance(points[0], float):
            fx1, fy1 = int(0.5 * (1 - points[0]) * w), int(0.5 * (1 - points[1]) * h)
            fx2, fy2 = int(0.5 * (1 + points[0]) * w), int(0.5 * (1 + points[1]) * h)
            cv2.rectangle(img, (fx1, fy1), (fx2, fy2), (0, 0, 255), 2)
            target.value = io.BytesIO(cv2.imencode('.png', img)[1]).getvalue()

EVENTS = {
    'get_date_list': get_date_list,
    'get_video_list': get_video_list,
    'get_sample_list': get_sample_list,
    'show_video_frame': show_video_frame,
    'focus_box_changed': focus_box_changed,
    'black_box_changed': black_box_changed,
    'center_rate_changed': center_rate_changed,
}