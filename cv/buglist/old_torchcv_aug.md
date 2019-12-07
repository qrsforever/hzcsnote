## Random Resized Crop

###  'int' object is not iterable
 
问题:
   
    datatrans.js默认类型错误, tuple --> int-list,  float-list
    
解决:

```
augmentation['random_resized_crop'].param = {"size":{name:'Size','type':'int-list','default':[32,32]},"scale_range":{name:'Scale Range','type':'float-list','default':[0.08, 1.0]},"aspect_range":{name:'Aspect Range','type':'float-list','default':[0.75, 1.33]}};
augmentation['random_resize'].param = {"ratio":{name:'ratio','type':'float','default':0.5},"scale_range":{name:'Scale Range','type':'float-list','default':[0.75, 1.25]},"aspect_range":{name:'Aspect Range','type':'float-list','default':[0.9, 1.1]}};

```


## Random Resize

### IndexError

```
2019-12-07T00:38:52.975346884Z INFO:tornado.access:200 POST /events (127.0.0.1) 1.22ms
2019-12-07T00:38:55.169865989Z Caught IndexError in DataLoader worker process 0.
2019-12-07T00:38:55.169939605Z Original Traceback (most recent call last):
2019-12-07T00:38:55.169958869Z   File "/usr/local/lib/python3.6/dist-packages/torch/utils/data/_utils/worker.py", line 178, in _worker_loop
2019-12-07T00:38:55.169966682Z     data = fetcher.fetch(index)
2019-12-07T00:38:55.169974298Z   File "/usr/local/lib/python3.6/dist-packages/torch/utils/data/_utils/fetch.py", line 44, in fetch
2019-12-07T00:38:55.169982034Z     data = [self.dataset[idx] for idx in possibly_batched_index]
2019-12-07T00:38:55.169988944Z   File "/usr/local/lib/python3.6/dist-packages/torch/utils/data/_utils/fetch.py", line 44, in <listcomp>
2019-12-07T00:38:55.170015334Z     data = [self.dataset[idx] for idx in possibly_batched_index]
2019-12-07T00:38:55.170022874Z   File "/hzcsk12/cauchy/datasets/cls/dataset/default_loader.py", line 60, in __getitem__
2019-12-07T00:38:55.170029861Z     img = self.aug_transform(img)
2019-12-07T00:38:55.170036541Z   File "/hzcsk12/cauchy/datasets/tools/cv2_aug_transforms.py", line 1580, in __call__
2019-12-07T00:38:55.170043638Z     img, labelmap, maskmap, kpts, bboxes, labels, polygons
2019-12-07T00:38:55.170050108Z   File "/hzcsk12/cauchy/datasets/tools/cv2_aug_transforms.py", line 708, in __call__
2019-12-07T00:38:55.170057101Z     scale_ratio = self.get_scale([width, height], bboxes)
2019-12-07T00:38:55.170065321Z   File "/hzcsk12/cauchy/datasets/tools/cv2_aug_transforms.py", line 641, in get_scale
2019-12-07T00:38:55.170072541Z     self.scale_range[0], self.scale_range[1]
2019-12-07T00:38:55.170079133Z IndexError: list index out of range

```
问题:

   配置参数错误 (二维)

解决:

Scale Range: 0.75,1.25
Aspect Range: 0.9,1.1

### AssertionError

```
2019-12-07T00:43:24.405678252Z INFO:tornado.access:200 POST /events (127.0.0.1) 0.99ms
2019-12-07T00:43:26.631528350Z Caught AssertionError in DataLoader worker process 0.
2019-12-07T00:43:26.631597952Z Original Traceback (most recent call last):
2019-12-07T00:43:26.631646649Z   File "/usr/local/lib/python3.6/dist-packages/torch/utils/data/_utils/worker.py", line 178, in _worker_loop
2019-12-07T00:43:26.631661232Z     data = fetcher.fetch(index)
2019-12-07T00:43:26.631668589Z   File "/usr/local/lib/python3.6/dist-packages/torch/utils/data/_utils/fetch.py", line 47, in fetch
2019-12-07T00:43:26.631676155Z     return self.collate_fn(data)
2019-12-07T00:43:26.631683012Z   File "/hzcsk12/cauchy/datasets/cls/data_loader.py", line 83, in <lambda>
2019-12-07T00:43:26.631691035Z     trans_dict=self.configer.get("train", "data_transformer")
2019-12-07T00:43:26.631698492Z   File "/hzcsk12/cauchy/datasets/tools/collate.py", line 204, in collate
2019-12-07T00:43:26.631705479Z     assert pad_height >= 0 and pad_width >= 0
2019-12-07T00:43:26.631712969Z AssertionError

```

问题: 

   增强scale变换导致size变化, pad校验出问题
   
解决:

   对齐方式(Align Method): Scale and Pad