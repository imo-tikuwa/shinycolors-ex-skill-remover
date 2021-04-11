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
import logging
import logzero
from logzero import logger
import configparser

# setting.ini関連
CONFIG_FILE = os.getcwd() + os.sep + 'settings.ini'
CONFIG_SECTION = 'default'
CONFIG_OPT_CHROME_EXECUTABLE_PATH = 'chrome_executable_path'
CONFIG_OPT_CHROME_REMOTE_DEBUGGING_PORT = 'remote_debugging_port'
CONFIG_OPT_EX_SKILL_BUTTON_ROI_LEFT = 'ex_skill_button_roi_left'
CONFIG_OPT_EX_SKILL_BUTTON_ROI_TOP = 'ex_skill_button_roi_top'
CONFIG_OPT_EX_SKILL_BUTTON_ROI_RIGHT = 'ex_skill_button_roi_right'
CONFIG_OPT_EX_SKILL_BUTTON_ROI_BOTTOM = 'ex_skill_button_roi_bottom'
CONFIG_OPT_EJECT_BUTTON_ROI_LEFT = 'eject_button_roi_left'
CONFIG_OPT_EJECT_BUTTON_ROI_TOP = 'eject_button_roi_top'
CONFIG_OPT_EJECT_BUTTON_ROI_RIGHT = 'eject_button_roi_right'
CONFIG_OPT_EJECT_BUTTON_ROI_BOTTOM = 'eject_button_roi_bottom'
CONFIG_OPT_PRODUCE_BUTTON_ROI_LEFT = 'produce_button_roi_left'
CONFIG_OPT_PRODUCE_BUTTON_ROI_TOP = 'produce_button_roi_top'
CONFIG_OPT_PRODUCE_BUTTON_ROI_RIGHT = 'produce_button_roi_right'
CONFIG_OPT_PRODUCE_BUTTON_ROI_BOTTOM = 'produce_button_roi_bottom'
CONFIG_OPT_PRODUCE_BUTTON_CLICK_LEFT = 'produce_button_click_left'
CONFIG_OPT_PRODUCE_BUTTON_CLICK_TOP = 'produce_button_click_top'
CONFIG_OPT_SUPPORT_BUTTON_CLICK_LEFT = 'support_button_click_left'
CONFIG_OPT_SUPPORT_BUTTON_CLICK_TOP = 'support_button_click_top'
CONFIG_OPT_PRODUCE_SEARCH_ROI_LEFT = 'produce_search_roi_left'
CONFIG_OPT_PRODUCE_SEARCH_ROI_TOP = 'produce_search_roi_top'
CONFIG_OPT_PRODUCE_SEARCH_ROI_RIGHT = 'produce_search_roi_right'
CONFIG_OPT_PRODUCE_SEARCH_ROI_BOTTOM = 'produce_search_roi_bottom'
CONFIG_OPT_EX_SKILL_SEARCH_ROI_LEFT = 'ex_skill_search_roi_left'
CONFIG_OPT_EX_SKILL_SEARCH_ROI_TOP = 'ex_skill_search_roi_top'
CONFIG_OPT_EX_SKILL_SEARCH_ROI_RIGHT = 'ex_skill_search_roi_right'
CONFIG_OPT_EX_SKILL_SEARCH_ROI_BOTTOM = 'ex_skill_search_roi_bottom'
CONFIG_OPT_EJECT_SEARCH_ROI_LEFT = 'eject_search_roi_left'
CONFIG_OPT_EJECT_SEARCH_ROI_TOP = 'eject_search_roi_top'
CONFIG_OPT_EJECT_SEARCH_ROI_RIGHT = 'eject_search_roi_right'
CONFIG_OPT_EJECT_SEARCH_ROI_BOTTOM = 'eject_search_roi_bottom'
CONFIG_OPT_EJECT_BUTTON_CLICK_LEFT = 'eject_button_click_left'
CONFIG_OPT_EJECT_BUTTON_CLICK_TOP = 'eject_button_click_top'
# setting.ini読み込み
SETTING_INI = configparser.ConfigParser()
SETTING_INI.read(CONFIG_FILE, 'cp932')
# ディレクトリ関連
RESOURCES_DIR = os.getcwd() + os.sep + 'resources' + os.sep
PRODUCE_EX_SKILL_DIR = RESOURCES_DIR + 'ex_skills' + os.sep + 'produce' + os.sep
SUPPORT_EX_SKILL_DIR = RESOURCES_DIR + 'ex_skills' + os.sep + 'support' + os.sep
EJECT_BUTTON_DIR = RESOURCES_DIR + 'eject_buttons' + os.sep
CARD_TYPE_BUTTON_DIR = RESOURCES_DIR + 'card_type_buttons' + os.sep
NPZ_FILE = RESOURCES_DIR + 'bundle.npz'
LOG_DIR = os.getcwd() + os.sep + 'log' + os.sep
LOG_FILE = LOG_DIR + 'application.log'
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
CARD_TYPE_BUTTON_NAMES = [
    'produce_on',
    'produce_off',
    'support_on',
    'support_off',
]
CARD_TYPE_TARGET_NAMES = [
    'produce',
    'support',
]
# 先頭キャラの1枠目
EX_SKILL_BUTTON_ROI = (
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EX_SKILL_BUTTON_ROI_LEFT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EX_SKILL_BUTTON_ROI_TOP),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EX_SKILL_BUTTON_ROI_RIGHT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EX_SKILL_BUTTON_ROI_BOTTOM),
)
# はずすボタン
EJECT_BUTTON_ROI = (
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_BUTTON_ROI_LEFT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_BUTTON_ROI_TOP),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_BUTTON_ROI_RIGHT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_BUTTON_ROI_BOTTOM),
)
# プロデュースボタン
PRODUCE_BUTTON_ROI = (
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_BUTTON_ROI_LEFT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_BUTTON_ROI_TOP),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_BUTTON_ROI_RIGHT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_BUTTON_ROI_BOTTOM),
)
# プロデュースボタンのクリック位置
PRODUCE_BUTTON_CLICK_LEFT = SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_BUTTON_CLICK_LEFT)
PRODUCE_BUTTON_CLICK_TOP = SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_BUTTON_CLICK_TOP)
# サポートボタンのクリック位置
SUPPORT_BUTTON_CLICK_LEFT = SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_SUPPORT_BUTTON_CLICK_LEFT)
SUPPORT_BUTTON_CLICK_TOP = SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_SUPPORT_BUTTON_CLICK_TOP)
# プロデュースボタンの探索範囲(固定秒待機をやめる用)
PRODUCE_SEARCH_ROI = (
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_SEARCH_ROI_LEFT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_SEARCH_ROI_TOP),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_SEARCH_ROI_RIGHT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_PRODUCE_SEARCH_ROI_BOTTOM),
)
# Exスキルの探索範囲
EX_SKILL_SEARCH_ROI = (
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EX_SKILL_SEARCH_ROI_LEFT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EX_SKILL_SEARCH_ROI_TOP),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EX_SKILL_SEARCH_ROI_RIGHT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EX_SKILL_SEARCH_ROI_BOTTOM),
)
# はずすボタンの探索範囲
EJECT_SEARCH_ROI = (
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_SEARCH_ROI_LEFT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_SEARCH_ROI_TOP),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_SEARCH_ROI_RIGHT),
    SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_SEARCH_ROI_BOTTOM),
)
# はずすボタンのクリック位置
EJECT_BUTTON_CLICK_LEFT = SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_BUTTON_CLICK_LEFT)
EJECT_BUTTON_CLICK_TOP = SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_EJECT_BUTTON_CLICK_TOP)

# ログディレクトリ、ログファイルを作成
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
logzero.logfile(LOG_FILE, encoding = "utf-8")
logzero.loglevel(logging.INFO)


def resource_path(filename):
    """
    exeファイル化に伴うリソースパスの動的な切り替えを行う関数
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(filename)


# npzファイル読み込み
NPZ_DATA = np.load(resource_path(NPZ_FILE), allow_pickle = True)
BINARY_PRODUCE_EX_SKILLS = NPZ_DATA['produce_ex_skills']
BINARY_SUPPORT_EX_SKILLS = NPZ_DATA['support_ex_skills']
BINARY_EJECT_BUTTONS = NPZ_DATA['eject_buttons']
BINARY_PRODUCE_ON_BUTTON = NPZ_DATA['produce_on_button']

def check_chrome_started():
    """
    GoogleChromeが41200ポートで起動してるかチェック
    """
    shiny_port_enabled = False
    remote_debugging_port = SETTING_INI.getint(CONFIG_SECTION, CONFIG_OPT_CHROME_REMOTE_DEBUGGING_PORT)
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN' and conn.laddr.port == remote_debugging_port:
            shiny_port_enabled = True
            break

    if not shiny_port_enabled:
        logger.error('{0}ポートでGoogleChromeが起動していません。exec_chrome.batよりGoogleChromeを起動してください'.format(remote_debugging_port))
        sys.exit(1)

    return shiny_port_enabled

def get_started_chrome():
    """
    ChromeDriverで起動中のGoogleChromeを取得
    """
    executable_path = SETTING_INI.get(CONFIG_SECTION, CONFIG_OPT_CHROME_EXECUTABLE_PATH)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:41200")
    driver = webdriver.Chrome(executable_path=executable_path, options=options)
    return driver