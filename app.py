# -*- coding: utf-8 -*-
import sys
import os
import click
import psutil
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from commons import *

if not check_chrome_started():
    print('41200ポートでChromeが起動していません。exec_chrome.batよりGoogleChromeを起動してください')
    sys.exit(1)

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:41200")
driver = webdriver.Chrome(executable_path='C:\\python\\chromedriver_win32\\chromedriver.exe', options=options)
driver.get("https://shinycolors.enza.fun/exSkill")
time.sleep(3)

try:
    canvas = driver.find_element_by_tag_name('canvas')
    while True:
        time.sleep(1)
        image = canvas.screenshot_as_png
        with open(TEMP_DIR + datetime.now().strftime("%Y%m%d%H%M%S") + '.png', 'wb') as f:
            f.write(image)
except KeyboardInterrupt:
    print('処理を中断しました')
    sys.exit(1)