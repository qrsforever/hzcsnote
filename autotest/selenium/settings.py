#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file settings.py
# @brief
# @author QRS
# @version 1.0
# @date 2020-12-13 16:07


import os
import xlrd


CUR_PATH = os.path.dirname(os.path.realpath(__file__))
TOP_PATH = os.path.dirname(CUR_PATH)
PRO_PATH = os.path.dirname(TOP_PATH)
OUTPUT_PATH = '/tmp/autotest'

# logger
LOG_ENABLED = True
LOG_STDOUT = True
LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s %(message)s'
LOG_PATH = os.path.join(OUTPUT_PATH, 'selenium.log')
LOG_PATH_BROWSER = os.path.join(OUTPUT_PATH, 'browser.log')

# browser
FIREFOX_BINARY_PATH = os.path.join('/usr/bin/', 'firefox')
FIREFOX_EXECUTABLE_PATH = os.path.join(TOP_PATH, 'bin', 'geckodriver')
FIREFOX_IMPLICITLY_WAIT = 3
FIREFOX_LOAD_TIMEOUT = 6000

# Home page
HOME_URL = 'http://app.hzcsai.com'

# element login xpath
LOGIN_USERNAME = '/html/body/div/section/main/div[1]/div/div[2]/form[1]/div[1]/div/div/input'
LOGIN_PASSWORD = '/html/body/div/section/main/div[1]/div/div[2]/form[1]/div[2]/div/div[1]/input'
LOGIN_CONFIRM = '/html/body/div/section/main/div[1]/div/div[2]/form[1]/div[3]/div/div'
LOGIN_SHOWNAME = '/html/body/div/div/div/section/header/div/div[3]/div/div/span'

# element course xpath
COURSES = {
    1: '/html/body/div/div/div/section/main/div/div[2]/div/div/div/div/div[1]/div[1]/div[2]',
    2: '/html/body/div/div/div/section/main/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]',
    3: '/html/body/div/div/div/section/main/div/div[2]/div/div/div/div/div[1]/div[3]/div[2]',
    4: '/html/body/div/div/div/section/main/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]',
    5: '/html/body/div/div/div/section/main/div/div[2]/div/div/div/div/div[1]/div[5]/div[2]',
    6: '/html/body/div/div/div/section/main/div/div[2]/div/div/div/div/div[1]/div[6]/div[2]',
}

# do gpu task
DO_TRAIN_NAVI = '/html/body/div/div/div/section/main/div/div[1]/div/div[4]/div[1]'
DO_TRAIN_START = '/html/body/div/div/div/section/main/div/div[2]/div/div/div/div[2]/div[1]/div/div[1]'
DO_TRAIN_PAUSE = '/html/body/div/div/div/section/main/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]'
DO_TRAIN_STOP = '/html/body/div/div/div/section/main/div/div[2]/div/div/div/div[2]/div[1]/div/div[3]'

DO_EVALUATE_NAVI = '/html/body/div/div/div/section/main/div/div[1]/div/div[5]/div[1]'
DO_EVALUATE_START = DO_TRAIN_START
DO_EVALUATE_STOP = DO_TRAIN_PAUSE

# users account

TEST_USERS = [
    ("999999999001", "111111"),
    ("999999999002", "111111"),
    ("999999999003", "111111"),
    ("999999999004", "111111"),
    ("999999999005", "111111"),
    ("999999999006", "111111"),
    ("999999999007", "111111"),
    ("999999999008", "111111"),
    ("999999999009", "111111"),
    ("999999999010", "111111"),
]

def _read_account_from_file(file):
    book = xlrd.open_workbook(f'{CUR_PATH}/{file}')
    sheet = book.sheet_by_index(0)
    users = []
    for rowid in range(1, sheet.nrows):
        username, password = sheet.row_values(rowid)
        users.append((username, str(password)[:-2]))
    return users

ACCOUNTS = _read_account_from_file

# CHANGESHA_21_USERS = _read_account_from_file('UA/长沙21中50人账号.xlsx')

# SHANDONG_JZYZ_USERS = _read_account_from_file('UA/山东胶州英姿学校40用户.xlsx')


if __name__ == "__main__":
    users = _read_account_from_file('UA/长沙21中50人账号.xlsx')
    print(users)
