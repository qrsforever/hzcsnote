#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file nb_dataset.py
# @brief
# @author QRS
# @version 1.0
# @date 2020-04-01 15:53

import os
import json
import torch # noqa
from PIL import Image
from torchvision import transforms
from torch.utils.data import (Dataset, DataLoader)


class ImageJsonFileDataset(Dataset):
    def __init__(self, datadir, jfiles, resize=None, transform=None):
        self.datadir = datadir
        self.resize = resize
        if isinstance(jfiles, str):
            jfiles = [jfiles]
        self.image_list, self.label_list = self.__read_json_file(jfiles)
        if transform:
            self.transform = transform
        else:
            self.transform = transforms.Compose([transforms.ToTensor()])

    def __getitem__(self, index):
        img = Image.open(self.image_list[index]).convert('RGB')
        print(img)
        if self.resize:
            img = img.resize(self.resize)
        if self.transform is not None:
            img = self.transform(img)
        return img, self.label_list[index], self.image_list[index]

    def __len__(self):
        return len(self.image_list)

    def __read_json_file(self, jfiles):
        image_list = []
        label_list = []
        for jfile in jfiles:
            with open(os.path.join(self.datadir, jfile)) as f:
                items = json.load(f)
                for item in items:
                    image_list.append(os.path.join(self.datadir, item['image_path']))
                    label_list.append(item['label'])
        return image_list, label_list


class ImageListFileDataset(Dataset):
    def __init__(self, imagelist, labellist=None, resize=(64, 64), transform=None):
        self.image_list = imagelist
        self.label_list = labellist
        self.resize = resize
        self.transform = transform
        if transform:
            self.transform = transform
        else:
            self.transform = transforms.Compose([transforms.ToTensor()])

    def __getitem__(self, index):
        img = Image.open(self.image_list[index]).convert('RGB')
        if self.resize:
            img = img.resize(self.resize)
        if self.transform is not None:
            img = self.transform(img)
        if self.label_list is not None:
            target = self.label_list[index]
        else:
            target = 0
        return img, target, self.image_list[index]

    def __len__(self):
        return len(self.image_list)


def k12ai_compute_mean_std(imagelist=None, labellist=None, datadir=None, jfiles=None):
    if imagelist is not None:
        dataset = ImageListFileDataset(imagelist=imagelist, labellist=labellist)
    else:
        dataset = ImageJsonFileDataset(datadir=datadir, jfiles=jfiles)
    loader = DataLoader(
        dataset,
        batch_size=64,
        num_workers=2,
        shuffle=False
    )

    mean = 0.
    std = 0.
    nb_samples = 0.
    
    for i, (data, label, path) in enumerate(loader):
        batch_samples = data.size(0)
        data = data.view(data.size(0), data.size(1), -1)
        mean += data.mean(2).sum(0)
        std += data.std(2).sum(0)
        nb_samples += batch_samples

    mean /= nb_samples
    std /= nb_samples

    return mean, std
