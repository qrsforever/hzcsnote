#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file browser.py
# @brief
# @author QRS
# @version 1.0
# @date 2020-12-13 16:43


from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from autotest.selenium.utils import Singleton
# from autotest.selenium.logger import Logger

import autotest.selenium.settings as settings


@Singleton
class Browser(object):
    # logger = Logger(__name__)
    driver = None

    def __init__(self, brw_name):
        if brw_name == 'firefox':
            profile = FirefoxProfile()
            self.driver = webdriver.Firefox(
                    firefox_profile = profile,
                    firefox_binary = settings.FIREFOX_BINARY_PATH,
                    executable_path = settings.FIREFOX_EXECUTABLE_PATH,
                    log_path = settings.LOG_PATH_BROWSER)
            self.driver.implicitly_wait(settings.FIREFOX_IMPLICITLY_WAIT)
            self.driver.set_page_load_timeout(settings.FIREFOX_LOAD_TIMEOUT)
            # self.driver.maximize_window()
        elif brw_name == 'chrome':
            # self.logger.warn('not impl')
            pass
        else:
            pass
            # self.logger.warn('not impl')

    def get_driver(self):
        return self.driver
