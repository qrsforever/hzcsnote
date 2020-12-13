#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import multiprocessing

import autotest.selenium.settings as settings

from autotest.selenium.browser import Browser
from autotest.selenium.utils import trycall


def do_login(browser, username, password):
    user_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_USERNAME))
    user_elem.clear()
    user_elem.send_keys(username)
    pswd_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_PASSWORD))
    pswd_elem.clear()
    pswd_elem.send_keys(password)

    btn_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_CONFIRM))
    btn_elem.click()
    time.sleep(4)


def do_course(browser, cid):
    btn_elem = trycall(lambda: browser.find_element_by_xpath(settings.COURSES[cid]))
    btn_elem.click()
    time.sleep(3)

    train_navi_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_TRAIN_NAVI))
    train_navi_elem.click()
    time.sleep(3)

    train_stop_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_TRAIN_STOP))
    train_stop_elem.click()
    time.sleep(3)

    train_start_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_TRAIN_START))
    train_start_elem.click()
    time.sleep(3)

    # stop
    time.sleep(300)
    train_stop_elem.click()


def process_task(username, password, cid):
    try:
        browser = Browser('firefox').get_driver()
        browser.get(settings.HOME_URL)
        do_login(browser, username, password)
        do_course(browser, cid)
    except Exception as e:
        print(e)
    finally:
        browser.quit()


if __name__ == "__main__":
    course = 1
    users = settings.TEST_USERS
    pool = multiprocessing.Pool(processes=len(users))
    process = []
    for username, password in users:
        time.sleep(3)
        process.append(pool.apply_async(process_task, (username, password, course)))
    pool.close()
    try:
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
