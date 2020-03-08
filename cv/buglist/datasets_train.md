## assert pad_height >= 0 and pad_width >= 0

```
2020-02-21 21:07:16,232 CRITICAL [main.py, 206] except: Caught AssertionError in DataLoader worker process 0.
Original Traceback (most recent call last):
  File "/usr/local/lib/python3.6/dist-packages/torch/utils/data/_utils/worker.py", line 178, in _worker_loop
    data = fetcher.fetch(index)
  File "/usr/local/lib/python3.6/dist-packages/torch/utils/data/_utils/fetch.py", line 47, in fetch
    return self.collate_fn(data)
  File "/hzcsk12/cv/torchcv/data/cls/data_loader.py", line 87, in <lambda>
    *args, trans_dict=self.configer.get('val', 'data_transformer')
  File "/hzcsk12/cv/torchcv/lib/data/collate.py", line 140, in collate
    assert pad_height >= 0 and pad_width >= 0
AssertionError
```


## DataLoader worker

```json
{'value': 'exiting',
 'way': 'crash',
 'errinfo': {'err_type': 'RuntimeError',
  'err_text': 'DataLoader worker (pid(s) 40) exited unexpectedly',
  'trackback': [{'filename': '/hzcsk12/cv/torchcv/main.py',
    'linenum': 194,
    'funcname': '<module>',
    'source': 'Controller.train(runner)'},
   {'filename': '/hzcsk12/cv/torchcv/lib/runner/controller.py',
    'linenum': 37,
    'funcname': 'train',
    'source': 'runner.train()'},
   {'filename': '/hzcsk12/cv/torchcv/runner/cls/image_classifier.py',
    'linenum': 104,
    'funcname': 'train',
    'source': 'for i, data_dict in enumerate(self.train_loader):'},
   {'filename': '/usr/local/lib/python3.6/dist-packages/torch/utils/data/dataloader.py',
    'linenum': 345,
    'funcname': '__next__',
    'source': 'data = self._next_data()'},
   {'filename': '/usr/local/lib/python3.6/dist-packages/torch/utils/data/dataloader.py',
    'linenum': 841,
    'funcname': '_next_data',
    'source': 'idx, data = self._get_data()'},
   {'filename': '/usr/local/lib/python3.6/dist-packages/torch/utils/data/dataloader.py',
    'linenum': 798,
    'funcname': '_get_data',
    'source': 'success, data = self._try_get_data()'},
   {'filename': '/usr/local/lib/python3.6/dist-packages/torch/utils/data/dataloader.py',
    'linenum': 774,
    'funcname': '_try_get_data',
    'source': "raise RuntimeError('DataLoader worker (pid(s) {}) exited unexpectedly'.format(pids_str))"}]}}
```

TODO:　Workers　设置为１ 或者启动container不去限制shm和mem
