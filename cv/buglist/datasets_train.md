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