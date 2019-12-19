#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file voc.py
# @brief
# @author QRS
# @version 1.0
# @date 2019-12-06 19:12:29

import json

SSD_VOC_CONFIG = json.loads('''{
    "dataset": "default",
    "task": "det",
    "method": "single_shot_detector",
    "data": {
      "num_classes": 21,
      "data_dir": "/data/datasets/cv/VOC07+12_DET",
      "image_tool": "cv2",
      "input_mode": "BGR",
      "keep_difficult": false,
      "workers": 1,
      "mean_value": [104, 117, 123],
      "normalize": {
        "div_value": 1,
        "mean": [104.0, 117.0, 123.0],
        "std": [1.0, 1.0, 1.0]
      }
    },
    "train": {
      "batch_size": 16,
      "aug_trans": {
        "shuffle_trans_seq": ["random_contrast", "random_hue", "random_saturation", "random_brightness", "random_perm"],
        "trans_seq": ["random_hflip", "random_pad", "random_det_crop"],
        "random_saturation": {
          "ratio": 0.5,
          "lower": 0.5,
          "upper": 1.5
        },
        "random_hue": {
          "ratio": 0.5,
          "delta": 18
        },
        "random_contrast": {
          "ratio": 0.5,
          "lower": 0.5,
          "upper": 1.5
        },
        "random_pad": {
          "ratio": 0.6,
          "up_scale_range": [1.0, 4.0]
        },
        "random_brightness": {
          "ratio": 0.5,
          "shift_value": 32
        },
        "random_perm": {
          "ratio": 0.5
        },
        "random_hflip": {
          "ratio": 0.5,
          "swap_pair": []
        },
        "random_det_crop":{
          "ratio": 1.0
        }
      },
      "data_transformer": {
        "size_mode": "fix_size",
        "input_size": [300, 300],
        "align_method": "only_scale"
      }
    },
    "val": {
      "batch_size": 16,
      "use_07_metric": true,
      "aug_trans": {
        "trans_seq": []
      },
      "data_transformer": {
        "size_mode": "fix_size",
        "input_size": [300, 300],
        "align_method": "only_scale"
      }
    },
    "test": {
      "batch_size": 16,
      "aug_trans": {
        "trans_seq": []
      },
      "data_transformer": {
        "size_mode": "fix_size",
        "input_size": [300, 300],
        "align_method": "only_scale"
      }
    },
    "anchor": {
      "anchor_method": "ssd",
      "iou_threshold": 0.5,
      "num_anchor_list": [4, 6, 6, 6, 4, 4],
      "feature_maps_wh": [[38, 38], [19, 19], [10, 10], [5, 5], [3, 3], [1, 1]],
      "cur_anchor_sizes": [30, 60, 111, 162, 213, 264, 315],
      "aspect_ratio_list": [[2], [2, 3], [2, 3], [2, 3], [2], [2]]
    },
    "details": {
      "color_list": [[255, 170, 30], [0, 0, 70], [244, 35, 232]],
      "name_id_dict": {
        "aeroplane": 1, "bicycle": 2, "bird": 3, "boat": 4, "bottle": 5, "bus": 6, "car": 7,
        "cat": 8, "chair": 9, "cow": 10, "diningtable": 11, "dog": 12, "horse": 13, "motorbike": 14,
        "person": 15, "pottedplant": 16, "sheep": 17, "sofa": 18, "train": 19, "tvmonitor": 20
      },
      "name_seq": ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair",
                   "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant",
                   "sheep", "sofa", "train", "tvmonitor"]
    },
    "network":{
      "backbone": "vgg16",
      "model_name": "vgg16_ssd300",
      "num_feature_list": [512, 1024, 512, 256, 256, 256],
      "stride_list": [8, 16, 30, 60, 100, 300],
      "head_index_list": [0, 1, 2, 3, 4, 5]
    },
    "solver": {
      "lr": {
        "metric": "epoch",
        "is_warm": true,
        "warm": {
          "warm_iters": 1000,
          "power": 1.0,
          "freeze_backbone": false
        },
        "base_lr": 0.001,
        "lr_policy": "multistep",
        "multistep": {
          "gamma": 0.1,
          "stepvalue": [156, 195, 234]
        }
      },
      "optim": {
        "optim_method": "sgd",
        "adam": {
          "betas": [0.9, 0.999],
          "eps": 1e-08,
          "weight_decay": 0.0001
        },
        "sgd":{
          "weight_decay": 0.0005,
          "momentum": 0.9,
          "nesterov": false
        }
      },
      "display_iter": 100,
      "save_iters": 5000,
      "test_interval": 5000,
      "max_epoch": 2
    },
    "res": {
      "nms": {
        "mode": "union",
        "max_threshold": 0.45,
        "pre_nms": 1000
      },
      "val_conf_thre": 0.01,
      "vis_conf_thre": 0.5,
      "max_per_image": 200,
      "cls_keep_num": 50
    },
    "loss": {
      "loss_type": "multibox_loss",
      "loss_weights": {
        "multibox_loss": {
            "multibox_loss": 1.0
        }
      }
    }
}''')

