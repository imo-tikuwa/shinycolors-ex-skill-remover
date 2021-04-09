# -*- coding: utf-8 -*-
import sys
import os
import click
import psutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER_PATH = 'C:\\python\\chromedriver_win32\\chromedriver.exe'
CHROME_PORT = 41200
RESOURCES_DIR = os.getcwd() + os.sep + 'resources' + os.sep
EX_SKILL_DIR = RESOURCES_DIR + 'exskills' + os.sep
LOG_DIR = os.getcwd() + os.sep + 'log' + os.sep
TEMP_DIR = os.getcwd() + os.sep + 'temp' + os.sep
EX_SKILL_IMAGE_NAMES = [
    # 初期値
    'init_vo',
    'init_da',
    'init_vi',
    'init_vovi',
    'init_davi',
    'init_voda',
    'init_all',
    'init_me',
    'init_sp',
    'init_dear'
    'init_tension',
    # 上限
    'limit_vo',
    'limit_da',
    'limit_vi',
    'limit_vovi',
    'limit_davi',
    'limit_voda',
    'limit_all',
    'limit_me',
    # 発生率
    'rate_morning',
    'rate_promise',
    'rate_trouble',
    'rate_perfect',
]

# Chromeが41200ポートで起動してるかチェック
def check_chrome_started():
    shiny_port_enabled = False
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN' and conn.laddr.port == CHROME_PORT:
            shiny_port_enabled = True
            break
    return shiny_port_enabled

# ChromeDriverで起動中のChromeを取得
def get_started_chrome():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:41200")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    return driver