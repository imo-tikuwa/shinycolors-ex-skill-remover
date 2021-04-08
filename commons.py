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

CHROME_PORT = 41200
RESOURCES_DIR = os.getcwd() + os.sep + 'resources' + os.sep
EX_SKILL_DIR = RESOURCES_DIR + 'exskills' + os.sep
LOG_DIR = os.getcwd() + os.sep + 'log' + os.sep
TEMP_DIR = os.getcwd() + os.sep + 'temp' + os.sep

# Chromeが41200ポートで起動してるかチェック
def check_chrome_started():
    shiny_port_enabled = False
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN' and conn.laddr.port == CHROME_PORT:
            shiny_port_enabled = True
            break
    return shiny_port_enabled