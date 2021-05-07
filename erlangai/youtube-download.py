import youtube_dl
import subprocess
import os
import csv
import pandas as pd
import tempfile
import random


YOUTUBE_PREFIX = 'https://www.youtube.com/watch?v='
DATASET_PREFIX = 'countix'

MODEL_Z_FRAMES = 64
REP_OUT_TIME = 0.5 # (repetition_start - REP_OUT_TIME, repetition_end + REP_OUT_TIME)
SOCKS5_PROXY = 'socks5://127.0.0.1:1881'

YDL_OPTS = {
    'format': 'mp4',
    'proxy': SOCKS5_PROXY,
    'quiet': True,
    'max_filesize': 30000000, # 30MB
}

def video_download_crop(vid, ss, to, frames_num, raw_dir, out_dir, force=False):
    raw_file = f'{raw_dir}/{vid}.mp4'
    out_file = f'{out_dir}/{vid}_{ss}_{to}.mp4'

    if os.path.exists(out_file):
        if force:
            os.remove(out_file)
        return out_file

    if not os.path.exists(raw_file):
        YDL_OPTS['outtmpl'] = raw_file
        with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
            ydl.download([f'{YOUTUBE_PREFIX}{vid}'])

    if os.path.exists(raw_file):
        cmd = 'ffmpeg -v 0 -i %s -s 112x112 -ss %s -to %s -frames %d -an %s' % (
                raw_file, ss, to, frames_num, out_file)
        subprocess.call(cmd, shell=True)
        return out_file

    return None

def data_preprocess(data_prefix, phase, force=False):
    df = pd.read_csv(f'{data_prefix}/countix_{phase}.csv')
    raw_dir = f'{data_prefix}/raw/{phase}'
    out_dir = f'{data_prefix}/{phase}'
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    df['file_name'] = ''
    df['rep_start_frame'] = 0
    df['rep_end_frame'] = 0
    for idx, row in df.iterrows():
        if phase == 'test' or phase == 'sample':
            vid, ks, ke, rs, re, count, file_name, rsf, rse = row
        else:
            vid, _, ks, ke, rs, re, count, file_name, rsf, rse = row

        cs = max([ks, rs - REP_OUT_TIME])
        ce = min([ke, re + REP_OUT_TIME])
        try:
            out_file = video_download_crop(vid, cs, ce,
                    MODEL_Z_FRAMES, raw_dir, out_dir, force)
            if out_file is not None:
                print('preprocess file: %s' % out_file)
                fps = MODEL_Z_FRAMES / (ce - cs)
                df.loc[idx, 'rep_start_frame'] = int(fps * (rs - cs))
                df.loc[idx, 'rep_end_frame'] = int(fps * (re - cs))
                df.loc[idx, 'file_name'] = os.path.basename(out_file)
            else:
                print('download or crop [%s] fail' % vid)
        except Exception as err:
            print('%s' % err)
    sub_df = df[df['file_name'].notnull()]
    sub_df.to_csv(f'{data_prefix}/sub_countix_{phase}.csv', index=False, header=True)
    return sub_df

if __name__ == "__main__":
    print('start')
    # data_preprocess(DATASET_PREFIX, 'sample')
    data_preprocess(DATASET_PREFIX, 'test')
    data_preprocess(DATASET_PREFIX, 'val')
    data_preprocess(DATASET_PREFIX, 'train')
    print('end!')

# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# url_prefix='https://www.youtube.com/watch?v='

# def download_video_from_url(vid, path_to_video='/tmp/video.mp4'):
#   if os.path.exists(path_to_video):
#     os.remove(path_to_video)
#   ydl_opts = {
#       # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
#       'format': 'mp4',
#       'outtmpl': str(path_to_video),
#       'proxy': 'socks5://127.0.0.1:1881',
#       'max_filesize': 30000000,
#   }
#   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     return ydl.download([f'{url_prefix}{vid}'])
#
#
# def clip_video(src_path, dst_path, start_time, end_time):
#     ffmpeg_extract_subclip(
#             src_path,
#             start_time,
#             end_time,
#             targetname=dst_path)
#
#
# def countix_download(phase):
#     path = f'countix/{phase}'
#     clip_path = f'clip/{phase}'
#     os.makedirs(path, exist_ok=True)
#     os.makedirs(clip_path, exist_ok=True)
#     count = 0
#     ferr = open(f'countix/error_{phase}.txt', 'w')
#     with open(f'countix/countix_{phase}.csv', 'r') as fw:
#         reader = csv.reader(fw)
#         # ['video_id', 'class', 'kinetics_start', 'kinetics_end', 'repetition_start', 'repetition_end', 'count']
#         next(reader)
#         for row in reader:
#             file = f'{path}/{row[0]}.mp4'
#             clip_file = f'{clip_path}/{row[0]}_{row[2]}_{row[3]}.mp4'
#             count += 1
#             try:
#                 if not os.path.exists(file):
#                     print(f'Download[{count}]: {file}')
#                     download_video_from_url(row[0], file)
#                 if not os.path.exists(clip_file) and os.path.exists(file):
#                     print(f'Clip {clip_file}')
#                     clip_video(file, clip_file, float(row[2]), float(row[3]))
#             except youtube_dl.utils.DownloadError as err:
#                 print('Download[%s] error' % row[0])
#                 ferr.write('%s\n' % row[0])
#     ferr.close()

# countix_download('val')
# countix_download('train')
# countix_download('test')

