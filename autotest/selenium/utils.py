#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file utils.py
# @brief
# @author QRS
# @blog qrsforever.gitee.io
# @version 1.0
# @date 2020-12-13 16:41

import time


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kwargs)
        return self._instance[self._cls]


def trycall(func, maxcnt = 6):
    while maxcnt > 0:
        try:
            return func()
        except Exception:
            time.sleep(1)
            maxcnt -= 1
