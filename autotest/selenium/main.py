#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path as osp
import time
import sys
import argparse
import multiprocessing

sys.path.append(osp.dirname(osp.dirname(osp.dirname(osp.realpath(__file__)))))

from autotest.selenium.browser import Browser
from autotest.selenium.utils import trycall
import autotest.selenium.settings as settings


def do_login(browser, username, password):
    user_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_USERNAME))
    user_elem.clear()
    user_elem.send_keys(username)
    pswd_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_PASSWORD))
    pswd_elem.clear()
    pswd_elem.send_keys(password)

    btn_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_CONFIRM))
    btn_elem.click()
    # browser.refresh()
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


def process_task(username, password, cid, time_s):
    try:
        browser = Browser('firefox').get_driver()
        browser.get(settings.HOME_URL)
        do_login(browser, username, password)
        do_course(browser, cid)
        time.sleep(time_s)
    except Exception as e:
        print(e)
    finally:
        stop_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_TRAIN_STOP))
        stop_elem.click()
        browser.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--config',
            default='test',
            type=str,
            dest='config',
            help="account configuration")
    parser.add_argument(
            '--course',
            default=1,
            type=int,
            dest='course',
            help="auto test which course")
    parser.add_argument(
            '--count',
            default=-1,
            type=int,
            dest='count',
            help="auto test user count")
    parser.add_argument(
            '--time',
            default=100,
            type=int,
            dest='time',
            help="auto test quit util time seconds")

    args = parser.parse_args()

    if args.config == 'test':
        users = settings.TEST_USERS[:args.count]
    else:
        users = settings.ACCOUNTS(args.config)[:args.count]
    pool = multiprocessing.Pool(processes=len(users))
    process = []
    for username, password in users:
        time.sleep(3)
        process.append(pool.apply_async(process_task, (
            username, password,
            args.course, args.time)))
    pool.close()
    try:
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
