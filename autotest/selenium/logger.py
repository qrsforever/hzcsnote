#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file logger.py
# @brief
# @author QRS
# @version 1.0
# @date 2020-12-13 16:33


import os
import logging
import autotest.selenium.settings as settings


class Logger(object):
    logger = None
    enable = settings.LOG_ENABLED

    def __init__(self, name):
        if not self.enable:
            return

        os.makedirs(settings.OUTPUT_PATH, exist_ok=True)
        logger = logging.getLogger(name)
        logger.setLevel(settings.LOG_LEVEL)
        formatter = logging.Formatter(settings.LOG_FORMAT)

        try:
            # file handler
            if settings.LOG_FILE:
                fh = logging.FileHandler(settings.LOG_PATH)
                fh.setFormatter(formatter)
                logger.addHandler(fh)
        except Exception:
            pass

        try:
            # console
            if settings.LOG_STDOUT:
                ch = logging.StreamHandler()
                ch.setFormatter(formatter)
                logger.addHandler(ch)
        except Exception:
            pass
        self.logger = logger

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.logger.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
