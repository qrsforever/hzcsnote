## GPU: TypeError: string indices must be integers

```
2020-01-23 14:39:49.695405  | k12_rl Running 300 sampler iterations.
2020-01-23 14:39:49.721743  | k12_rl Frame-based buffer using 4-frame sequences.
2020-01-23 14:42:01.563911  | k12_rl Agent setting min/max epsilon itrs: 97, 1953
QRS:startup2
QRS:launch_workers
QRS:  {'all_cpus': (0, 1, 2, 3, 4, 5, 6, 7), 'optimizer': [{'cpus': (0,), 'cuda_idx': 0, 'torch_threads': 1, 'set_affinity': True}], 'sampler': {'all_cpus': (1, 2, 3, 4, 5, 6, 7), 'master_cpus': (1, 2, 3, 4, 5, 6, 7), 'workers_cpus': ((1,), (2,), (3,), (4,), (5,), (6,), (7,)), 'master_torch_threads': 7, 'worker_torch_threads': 1, 'cuda_idx': None, 'alternating': False, 'set_affinity': True}, 'set_affinity': True}
2020-01-23 14:42:04.741861  | k12_rl Optimizer master CPU affinity: [0].
2020-01-23 14:42:05.294611  | k12_rl Optimizer master Torch threads: 1.
QRS:0run_async_sampler: 300
Process Process-5:
Traceback (most recent call last):
  File "/usr/lib/python3.6/multiprocessing/process.py", line 258, in _bootstrap
    self.run()
  File "/usr/lib/python3.6/multiprocessing/process.py", line 93, in run
    self._target(*self._args, **self._kwargs)
  File "/hzcsk12/rl/rlpyt/rlpyt/runners/async_rl.py", line 441, in run_async_sampler
    sampler.initialize(affinity)
  File "/hzcsk12/rl/rlpyt/rlpyt/samplers/async_/gpu_sampler.py", line 34, in initialize
    n_envs_lists = self._get_n_envs_lists(affinity)
  File "/hzcsk12/rl/rlpyt/rlpyt/samplers/async_/gpu_sampler.py", line 68, in _get_n_envs_lists
    n_workers = [len(aff["workers_cpus"]) for aff in affinity]
  File "/hzcsk12/rl/rlpyt/rlpyt/samplers/async_/gpu_sampler.py", line 68, in <listcomp>
    n_workers = [len(aff["workers_cpus"]) for aff in affinity]
TypeError: string indices must be integers
2020-01-23 14:42:13.535962  | k12_rl Initialized agent model on device: cuda:0.
2020-01-23 14:42:13.544566  | k12_rl Optimizing over 3 sampler iterations.
```


## CPU: AttributeError: 'tuple' object has no attribute 'env'

```
Traceback (most recent call last):
  File "/usr/lib/python3.6/multiprocessing/process.py", line 258, in _bootstrap
    self.run()
  File "/usr/lib/python3.6/multiprocessing/process.py", line 93, in run
    self._target(*self._args, **self._kwargs)
  File "/hzcsk12/rl/rlpyt/rlpyt/samplers/parallel/worker.py", line 49, in sampling_process
    env_ranks=w.get("env_ranks", None),
  File "/hzcsk12/rl/rlpyt/rlpyt/samplers/async_/collectors.py", line 11, in __init__
    super().__init__(*args, **kwargs)
  File "/hzcsk12/rl/rlpyt/rlpyt/samplers/parallel/cpu/collectors.py", line 67, in __init__
    self.samples_np.env.observation[0, :len(self.envs)], "copy")
AttributeError: 'tuple' object has no attribute 'env'
Process Process-5:3:
```

> mid batch reset : false