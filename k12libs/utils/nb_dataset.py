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
import numpy as np # noqa
import random
from PIL import Image
from torchvision import transforms, models
from torch.utils.data import (Dataset, DataLoader)
from .nb_easy import k12ai_get_top_dir, K12AI_PRETRAINED_ROOT


class ImageJsonFileDataset(Dataset):
    def __init__(self, datadir, jfiles, resize=(224, 224), transform=None):
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


def k12ai_compute_mean_std(imagelist=None, labellist=None, datadir=None, jfiles=None, resize=(224, 224)):
    if imagelist is not None:
        dataset = ImageListFileDataset(imagelist=imagelist, labellist=labellist, resize=resize)
    else:
        dataset = ImageJsonFileDataset(datadir=datadir, jfiles=jfiles, resize=resize)
    loader = DataLoader(
        dataset,
        batch_size=32,
        num_workers=1,
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

    mean = [round(x, 4) for x in mean.numpy().tolist()]
    std = [round(x, 4) for x in std.numpy().tolist()]
    return mean, std


def k12ai_generate_jsonfiles(img_path):
    label_image_dict = {}
    with os.scandir(img_path) as it:
        for entry in it:
            if not entry.is_dir():
                continue
            label_image_dict[entry.name] = []
            with os.scandir(os.path.join(entry.path)) as imgit:
                for imgentry in imgit:
                    if not imgentry.is_file():
                        continue
                    label_image_dict[entry.name].append(imgentry.path)

    def _gen_json_file(images, phase):
        prefix = len(img_path) + 1
        items = []
        for label, img in images:
            items.append({'image_path': img[prefix:], 'label': int(label)})

        random.shuffle(items)

        jsonfile = os.path.join(img_path, f'{phase}.json')
        with open(jsonfile, 'w') as fp:
            json.dump(items, fp)
        return len(items)

    def _split_data(label_images):
        # 6:2:2 split for train:valid:test dataset
        all_images = []
        test_images = []
        valid_images = []
        train_images = []
        for i, (label, files) in enumerate(label_images.items()):
            for img in files:
                all_images.append((i, img))
                value = random.random()
                if value < 0.2: # test
                    test_images.append((i, img))
                elif value < 0.4: # val
                    valid_images.append((i, img))
                else: # train
                    train_images.append((i, img))
        return all_images, train_images, valid_images, test_images

    d_all, d_train, d_valid, d_test = _split_data(label_image_dict)

    _gen_json_file(d_all, 'all')
    _gen_json_file(d_train, 'train')
    _gen_json_file(d_valid, 'val')
    _gen_json_file(d_test, 'test')

    mean, std = k12ai_compute_mean_std(datadir=img_path, jfiles='all.json', resize=(224, 224))

    info = {
        'num_records': len(d_all),
        'num_classes': len(label_image_dict),
        'label_names': list(label_image_dict.keys()),
        'mean': mean,
        'std': std,
    }

    with open(os.path.join(img_path, 'info.json'), 'w') as fw:
        json.dump(info, fw, indent=4)

    return info


def k12ai_load_image(path, resize=None, mean=None, std=None, cuda=True):
    if not os.path.isfile(path):
        path = os.path.join(k12ai_get_top_dir(), 'assets', path)

    raw_image = Image.open(path).convert('RGB')
    if resize:
        raw_image = raw_image.resize(resize)

    # image = transforms.ToTensor()(np.array(raw_image).astype(np.uint8))
    image = transforms.ToTensor()(raw_image)
    if mean and std:
        image = transforms.Normalize(mean, std)(image)

    if cuda:
        image = image.cuda()
    return image, raw_image

def k12ai_load_model(name, pretrained=True, cuda=True):
    if name == 'vgg16':
        model = models.vgg16(pretrained=False)
        pretrained_file = 'vgg16-397923af.pth'
    elif name == 'resnet50':
        model = models.resnet50(pretrained=False)
        pretrained_file = 'resnet50-19c8e357.pth'
    elif name == 'resnet152':
        model = models.resnet152(pretrained=False)
        pretrained_file = 'resnet152-b121ed2d.pth'
    elif name == 'alexnet':
        model = models.alexnet(pretrained=False)
        pretrained_file = 'alexnet-owt-4df8aa71.pth'
    else:
        return None

    if pretrained:
        state = torch.load(os.path.join(K12AI_PRETRAINED_ROOT, 'cv', pretrained_file))
        model.load_state_dict(state)
    if cuda:
        model = model.cuda()
    return model
