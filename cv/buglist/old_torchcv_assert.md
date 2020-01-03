2019-12-26T04:20:06.519870082Z /pytorch/aten/src/THCUNN/ClassNLLCriterion.cu:105: void cunn_ClassNLLCriterion_updateOutput_kernel(Dtype *, Dtype *, Dtype *, long *, Dtype *, int, int, int, int, long) [with Dtype = float, Acctype = float]: block: [0,0,0], thread: [30,0,0] Assertion `t >= 0 && t < n_classes` failed.
2019-12-26T04:20:06.519877487Z /pytorch/aten/src/THCUNN/ClassNLLCriterion.cu:105: void cunn_ClassNLLCriterion_updateOutput_kernel(Dtype *, Dtype *, Dtype *, long *, Dtype *, int, int, int, int, long) [with Dtype = float, Acctype = float]: block: [0,0,0], thread: [31,0,0] Assertion `t >= 0 && t < n_classes` failed.

2019-12-26T04:20:09.142365393Z CUDA error: device-side assert triggered


原因: nn.CrossEntropyLoss(input, target)中, input的列数和target不匹配

2019-12-26T04:31:31.188830534Z QRSDEL shape:  <class 'torch.Tensor'> torch.Size([32, 29563]) tensor([124769, 188410,  24382, 103036, 113747,  80692, 104497, 139894, 103232,
2019-12-26T04:31:31.188847324Z         159237,  30675, 169983,  35564, 139894, 162417, 118492,  15859,  52422,
2019-12-26T04:31:31.188853756Z          41310,  65165, 149917, 155479, 129164,  62978, 187817,  83416,  72550,
2019-12-26T04:31:31.188859701Z         154764, 148490, 160557, 201661, 113359], device='cuda:0')
