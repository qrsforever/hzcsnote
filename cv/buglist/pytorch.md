# RuntimeError: ONNX export failed: Couldn't export operator aten::avg_pool2d

see: https://github.com/onnx/tutorials/issues/63


# subprocess.CalledProcessError: Command '['ninja', '-v']' returned non-zero exit status 1.

see: https://github.com/open-mmlab/mmdetection/pull/2524


# ModuleNotFoundError: No module named 'models'

```
>>> import torch
>>> torch.load('/data/cv3d/model_best.pth.tar')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.6/site-packages/torch/serialization.py", line 426, in load
    return _load(f, map_location, pickle_module, **pickle_load_args)
  File "/usr/local/lib/python3.6/site-packages/torch/serialization.py", line 613, in _load
    result = unpickler.load()
ModuleNotFoundError: No module named 'models'
```

see:　　https://github.com/pytorch/pytorch/issues/18325


# UserWarning: The given NumPy array is not writeable

```
/pytorch/torch/csrc/utils/tensor_numpy.cpp:141: UserWarning: The given NumPy array is not writeable, and PyTorch does not support non-writeable tensors. This means you can write to the underlying (supposedly non-writeable) NumPy array using the tensor. You may want to copy the array to protect its data or make it writeable before converting it to a tensor. This type of warning will be suppressed for the rest of this program.
```

see: https://discuss.pytorch.org/t/userwarning-the-given-numpy-array-is-not-writeable/78748/7