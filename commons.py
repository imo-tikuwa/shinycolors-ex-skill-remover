# -*- coding: utf-8 -*-
import sys
import os
import click
import psutil
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def resource_path(filename):
    # exeファイル化に伴うリソースパスの動的な切り替えを行う関数
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(filename)

CHROME_DRIVER_PATH = 'C:\\python\\chromedriver_win32\\chromedriver.exe'
CHROME_PORT = 41200
RESOURCES_DIR = os.getcwd() + os.sep + 'resources' + os.sep
PRODUCE_EX_SKILL_DIR = RESOURCES_DIR + 'ex_skills' + os.sep + 'produce' + os.sep
SUPPORT_EX_SKILL_DIR = RESOURCES_DIR + 'ex_skills' + os.sep + 'support' + os.sep
EJECT_BUTTON_DIR = RESOURCES_DIR + 'eject_buttons' + os.sep
NPZ_FILE = RESOURCES_DIR + 'bundle.npz'
LOG_DIR = os.getcwd() + os.sep + 'log' + os.sep
TEMP_DIR = os.getcwd() + os.sep + 'temp' + os.sep
PRODUCE_EX_SKILL_NAMES = [
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
    'init_dear',
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
SUPPORT_EX_SKILL_NAMES = [
    # ステータス
    'status_vo',
    'status_da',
    'status_vi',
    'status_vovi',
    'status_davi',
    'status_voda',
    'status_all',
    'status_me',
    # 滞在率
    'stay_vo',
    'stay_da',
    'stay_vi',
    'stay_ra',
    'stay_ta',
    'stay_ma',
    # その他
    'kizuna',
    'support',
]
EJECT_BUTTON_NAMES = [
    'eject_on',
    # 外すボタンについて「非活性のとき」と「表示されてないとき」の画像は不要だった。
    # 以下は一旦コメントアウトし、resources以下のサンプル画像は削除する。
    # 'eject_off',
    # 'eject_none',
]
# 先頭キャラの1枠目
EX_SKILL_BUTTON_ROI = (255, 254, 344, 343)
# 「はずす」ボタン
EJECT_BUTTON_ROI = (1169, 811, 1386, 914)
# Exスキルの探索範囲
EX_SKILL_SEARCH_LEFT = 240
EX_SKILL_SEARCH_TOP = 210
EX_SKILL_SEARCH_ROI = (EX_SKILL_SEARCH_LEFT, EX_SKILL_SEARCH_TOP, 620, 800)
EJECT_SEARCH_ROI = (1147, 800, 1409, 932)
EJECT_BUTTON_CLICK_LEFT = 1269
EJECT_BUTTON_CLICK_TOP = 865


# npzファイル読み込み
NPZ_DATA = np.load(resource_path(NPZ_FILE), allow_pickle = True)
BINARY_PRODUCE_EX_SKILLS = NPZ_DATA['produce_ex_skills']
BINARY_SUPPORT_EX_SKILLS = NPZ_DATA['support_ex_skills']
BINARY_EJECT_BUTTONS = NPZ_DATA['eject_buttons']

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
