#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file custom_ssd.py
# @brief
# @author QRS
# @version 1.0
# @date 2020-02-05 19:19


NETWORK_BACKBONE_DEF = '''plain_net {
    name: "det_7b6a035dfb085fca2dd9bc35939b8add"
     
    layer{
      conv{
        name : "Conv2d_6018"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "x"
        outputs : "Relu_8759"
        layer_params {
          in_channels : "3"
          out_channels : "64"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_8759"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_6018"
        outputs : "Conv2d_9065"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_9065"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "Relu_8759"
        outputs : "Relu_3620"
        layer_params {
          in_channels : "64"
          out_channels : "64"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_3620"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_9065"
        outputs : "MaxPool2d_8137"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      pool{
        name : "MaxPool2d_8137"
        layer_builder : "NNTorchLayer"
        layer_mode : MAXPOOL2D
        inputs : "Relu_3620"
        outputs : "Conv2d_1217"
        layer_params {
          kernel_size : "2"
          stride : "2"
          ceil_mode : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_1217"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "MaxPool2d_8137"
        outputs : "Relu_1020"
        layer_params {
          in_channels : "64"
          out_channels : "128"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_1020"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_1217"
        outputs : "Conv2d_4367"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_4367"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "Relu_1020"
        outputs : "Relu_4518"
        layer_params {
          in_channels : "128"
          out_channels : "128"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_4518"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_4367"
        outputs : "MaxPool2d_6358"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      pool{
        name : "MaxPool2d_6358"
        layer_builder : "NNTorchLayer"
        layer_mode : MAXPOOL2D
        inputs : "Relu_4518"
        outputs : "Conv2d_3526"
        layer_params {
          kernel_size : "2"
          stride : "2"
          ceil_mode : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_3526"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "MaxPool2d_6358"
        outputs : "Relu_2841"
        layer_params {
          in_channels : "128"
          out_channels : "256"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_2841"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_3526"
        outputs : "Conv2d_4763"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_4763"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "Relu_2841"
        outputs : "Relu_2199"
        layer_params {
          in_channels : "256"
          out_channels : "256"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_2199"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_4763"
        outputs : "Conv2d_6272"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_6272"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "Relu_2199"
        outputs : "Relu_2306"
        layer_params {
          in_channels : "256"
          out_channels : "256"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_2306"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_6272"
        outputs : "MaxPool2d_3269"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      pool{
        name : "MaxPool2d_3269"
        layer_builder : "NNTorchLayer"
        layer_mode : MAXPOOL2D
        inputs : "Relu_2306"
        outputs : "Conv2d_9436"
        layer_params {
          kernel_size : "2"
          stride : "2"
          ceil_mode : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_9436"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "MaxPool2d_3269"
        outputs : "Relu_3155"
        layer_params {
          in_channels : "256"
          out_channels : "512"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_3155"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_9436"
        outputs : "Conv2d_4320"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_4320"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "Relu_3155"
        outputs : "Relu_5503"
        layer_params {
          in_channels : "512"
          out_channels : "512"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_5503"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_4320"
        outputs : "Conv2d_6001"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_6001"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "Relu_5503"
        outputs : "Relu_2697"
        layer_params {
          in_channels : "512"
          out_channels : "512"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_2697"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_6001"
        outputs : "MaxPool2d_8588"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      pool{
        name : "MaxPool2d_8588"
        layer_builder : "NNTorchLayer"
        layer_mode : MAXPOOL2D
        inputs : "Relu_2697"
        outputs : "Conv2d_1211"
        layer_params {
          kernel_size : "2"
          stride : "2"
          ceil_mode : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_1211"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "MaxPool2d_8588"
        outputs : "Relu_5533"
        layer_params {
          in_channels : "512"
          out_channels : "512"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_5533"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_1211"
        outputs : "Conv2d_8034"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_8034"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "Relu_5533"
        outputs : "Relu_5816"
        layer_params {
          in_channels : "512"
          out_channels : "512"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_5816"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_8034"
        outputs : "Conv2d_1342"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_1342"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "Relu_5816"
        outputs : "Relu_4359"
        layer_params {
          in_channels : "512"
          out_channels : "512"
          kernel_size : "3"
          padding : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_4359"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_1342"
        outputs : "MaxPool2d_6276"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      pool{
        name : "MaxPool2d_6276"
        layer_builder : "NNTorchLayer"
        layer_mode : MAXPOOL2D
        inputs : "Relu_4359"
        outputs : "Conv2d_7495"
        layer_params {
          kernel_size : "3"
          stride : "1"
          padding : "1"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_7495"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "MaxPool2d_6276"
        outputs : "Relu_3916"
        layer_params {
          in_channels : "512"
          out_channels : "1024"
          kernel_size : "3"
          padding : "6"
          dilation : "6"
        }
      }
    }
    layer{
      act{
        name : "Relu_3916"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_7495"
        outputs : "Conv2d_4286"
        layer_params {
          inplace : "True"
        }
      }
    }
    layer{
      conv{
        name : "Conv2d_4286"
        layer_builder : "NNTorchLayer"
        layer_mode : CONV2D
        inputs : "Relu_3916"
        outputs : "Relu_2931"
        layer_params {
          in_channels : "1024"
          out_channels : "1024"
          kernel_size : "1"
        }
      }
    }
    layer{
      act{
        name : "Relu_2931"
        layer_builder : "NNTorchLayer"
        layer_mode : RELU
        inputs : "Conv2d_4286"
        layer_params {
          inplace : "True"
        }
      }
    }
}'''
