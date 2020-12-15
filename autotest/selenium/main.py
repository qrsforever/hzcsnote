#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path as osp
import time
import sys
import argparse
import traceback
import multiprocessing

from xvfbwrapper import Xvfb

sys.path.append(osp.dirname(osp.dirname(osp.dirname(osp.realpath(__file__)))))

from autotest.selenium.browser import Browser
from autotest.selenium.utils import trycall
from autotest.selenium.logger import Logger

import autotest.selenium.settings as settings

logger = Logger('autotest.selenium')


def do_login(browser, username, password):
    logger.info(f'login username: {username}')
    user_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_USERNAME))
    user_elem.clear()
    user_elem.send_keys(username)
    pswd_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_PASSWORD))
    pswd_elem.clear()
    pswd_elem.send_keys(password)

    btn_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_CONFIRM))
    btn_elem.click()

    show_elem = trycall(lambda: browser.find_element_by_xpath(settings.LOGIN_SHOWNAME))
    browser.execute_script("arguments[0].innerHTML = arguments[1];", show_elem, username[-3:])
    # show_elem.send_keys(username) # Error: is not reachable by keyboard

    time.sleep(4)
    


def do_course(browser, cid, train_time):
    logger.info(f'course: {cid}')
    btn_elem = trycall(lambda: browser.find_element_by_xpath(settings.COURSES[cid]))
    btn_elem.click()
    time.sleep(3)

    # train
    if train_time > 0:
        train_navi_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_TRAIN_NAVI))
        train_navi_elem.click()
        time.sleep(3)

        train_stop_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_TRAIN_STOP))
        train_stop_elem.click()
        time.sleep(3)

        train_start_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_TRAIN_START))
        train_start_elem.click()
        time.sleep(3)

        time.sleep(train_time)
        train_stop_elem.click()
        time.sleep(8)

    # evaluate
    evaluate_navi_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_EVALUATE_NAVI))
    evaluate_navi_elem.click()
    time.sleep(3)

    evaluate_stop_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_EVALUATE_STOP))
    evaluate_stop_elem.click()
    time.sleep(3)

    evaluate_start_elem = trycall(lambda: browser.find_element_by_xpath(settings.DO_EVALUATE_START))
    evaluate_start_elem.click()
    time.sleep(20)
    evaluate_stop_elem.click()
    time.sleep(3)


def process_task(username, password, cid, train_time):
    # with Xvfb(width=800, height=600, colordepth=24) as xvfb: # noqa
    browser = Browser('firefox').get_driver()
    browser.get(settings.HOME_URL)
    try:
        do_login(browser, username, password)
        do_course(browser, cid, train_time)
    except Exception:
        logger.error(traceback.format_exc())
    finally:
        browser.quit()


if __name__ == "__main__":
    def str2bool(v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Unsupported value encountered.')

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
            '--range',
            default='0:1',
            type=str,
            dest='range',
            help="auto test user range[a:b]")
    parser.add_argument(
            '--train_time',
            default=200,
            type=int,
            dest='train_time',
            help="auto test quit util train time seconds")
    parser.add_argument(
            '--xvfb',
            default=False,
            type=str2bool,
            dest='xvfb',
            help="auto test using xvfb virtual display")

    args = parser.parse_args()
    if args.xvfb:
        xvfb = Xvfb(width=800, height=600, colordepth=24)
        xvfb.start()

    _from, _to = args.range.split(':')

    if args.config == 'test':
        users = settings.TEST_USERS[int(_from):int(_to)]
    else:
        users = settings.ACCOUNTS(args.config)[int(_from):int(_to)]
    pool = multiprocessing.Pool(processes=len(users))
    process = []
    for username, password in users:
        time.sleep(2)
        process.append(pool.apply_async(process_task, (
            username, password,
            args.course, args.train_time)))
    pool.close()
    try:
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
    finally:
        if args.xvfb:
            xvfb.stop()
