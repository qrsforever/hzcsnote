#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file nb_ai.py
# @brief
# @author QRS
# @version 1.0
# @date 2020-07-11 09:55


import argparse
from collections import OrderedDict
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, Generator, Union

from torch.nn import Module

import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from pytorch_lightning import _logger as log
from torch import optim
from torch.optim.lr_scheduler import MultiStepLR
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader
from torchvision import models
from torchvision import transforms
from torchvision.datasets import ImageFolder
