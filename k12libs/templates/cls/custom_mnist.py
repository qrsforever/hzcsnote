#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file custom_mnist.py
# @brief
# @author QRS
# @version 1.0
# @date 2020-02-06 17:33


NETWORK_MNIST_DEF = '''plain_net {
name: "cls_423fe4f31e09d4498d7e56f771488dab"

layer{
  conv{
    name : "Conv2d_7284"
    layer_builder : "NNTorchLayer"
    layer_mode : CONV2D
    inputs : "x"
    outputs : "Conv2d_8260"
    layer_params {
      in_channels : "3"
      out_channels : "30"
      kernel_size : "3"
    }
  }
}
layer{
  conv{
    name : "Conv2d_8260"
    layer_builder : "NNTorchLayer"
    layer_mode : CONV2D
    inputs : "Conv2d_7284"
    outputs : "Conv2d_6293"
    layer_params {
      in_channels : "30"
      out_channels : "30"
      kernel_size : "3"
    }
  }
}
layer{
  conv{
    name : "Conv2d_6293"
    layer_builder : "NNTorchLayer"
    layer_mode : CONV2D
    inputs : "Conv2d_8260"
    outputs : "MaxPool2d_6160"
    layer_params {
      in_channels : "30"
      out_channels : "30"
      kernel_size : "3"
    }
  }
}
layer{
  pool{
    name : "MaxPool2d_6160"
    layer_builder : "NNTorchLayer"
    layer_mode : MAXPOOL2D
    inputs : "Conv2d_6293"
    outputs : "Conv2d_7630"
    layer_params {
      kernel_size : "3"
      stride : "1"
    }
  }
}
layer{
  conv{
    name : "Conv2d_7630"
    layer_builder : "NNTorchLayer"
    layer_mode : CONV2D
    inputs : "MaxPool2d_6160"
    outputs : "MaxPool2d_4146"
    layer_params {
      in_channels : "30"
      out_channels : "50"
      kernel_size : "3"
    }
  }
}
layer{
  pool{
    name : "MaxPool2d_4146"
    layer_builder : "NNTorchLayer"
    layer_mode : MAXPOOL2D
    inputs : "Conv2d_7630"
    outputs : "Flatten_2327"
    layer_params {
      kernel_size : "3"
      stride : "1"
    }
  }
}
layer{
  vulkan{
    name : "Flatten_2327"
    layer_builder : "NNTorchLayer"
    layer_mode : FLATTEN
    inputs : "MaxPool2d_4146"
    outputs : "Linear_9679"
    layer_params {
      start_dim : "1"
    }
  }
}
layer{
  linear{
    name : "Linear_9679"
    layer_builder : "NNTorchLayer"
    layer_mode : LINEAR
    inputs : "Flatten_2327"
    outputs : "Linear_2415"
    layer_params {
      in_features : "12800"
      out_features : "500"
    }
  }
}
layer{
  linear{
    name : "Linear_2415"
    layer_builder : "NNTorchLayer"
    layer_mode : LINEAR
    inputs : "Linear_9679"
    outputs : "Linear_3966"
    layer_params {
      in_features : "500"
      out_features : "100"
    }
  }
}
layer{
  linear{
    name : "Linear_3966"
    layer_builder : "NNTorchLayer"
    layer_mode : LINEAR
    inputs : "Linear_2415"
    outputs : "Output_5560"
    layer_params {
      in_features : "100"
      out_features : "10"
    }
  }
}
}'''
