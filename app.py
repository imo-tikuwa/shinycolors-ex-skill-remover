# -*- coding: utf-8 -*-
import sys
import os
import click
import psutil
import time
from datetime import datetime
from commons import *

if not check_chrome_started():
    print('41200ポートでChromeが起動していません。exec_chrome.batよりGoogleChromeを起動してください')
    sys.exit(1)

driver = get_started_chrome()
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