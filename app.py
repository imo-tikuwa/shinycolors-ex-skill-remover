# -*- coding: utf-8 -*-
import sys
import os
import click
import psutil
import time
from datetime import datetime
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
from selenium.webdriver.common.action_chains import ActionChains
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
        time.sleep(0.5)

        # temp_name = TEMP_DIR + datetime.now().strftime("%Y%m%d%H%M%S")
        original_image = canvas.screenshot_as_png
        # with open(temp_name + '_org.png', 'wb') as f:
        #     f.write(original_image)
        original_image = Image.open(BytesIO(original_image))

        # 「はずす」ボタンの辺りをざっくり切り抜いた画像を作成
        eject_button_image = original_image.crop(EJECT_SEARCH_ROI)
        # eject_button_image.save(temp_name + '_cropped_eject_area1.png')
        eject_button_frame = np.asarray(eject_button_image)
        eject_button_frame = cv2.cvtColor(eject_button_frame, cv2.COLOR_RGB2BGR)
        # cv2.imwrite(temp_name + '_cropped_eject_area2.png', eject_button_frame)

        # 「はずす」ボタンが表示されてたらクリック。
        # カラー画像でテンプレートマッチング
        # ボタンが存在したら後続のExスキル枠のマッチングを行わずに次のループに移動
        exist_eject_button = False
        for num, template_img in enumerate(BINARY_EJECT_BUTTONS):
            res = cv2.matchTemplate(eject_button_frame, template_img, cv2.TM_CCORR_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if (max_val > 0.99):
                exist_eject_button = True
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(canvas, EJECT_BUTTON_CLICK_LEFT, EJECT_BUTTON_CLICK_TOP)
                actions.click()
                actions.perform()
                break
        if exist_eject_button:
            continue


        # Exスキルの1～3枠×4列分くらいの領域を切り抜いた画像を作成
        ex_skill_image = original_image.crop(EX_SKILL_SEARCH_ROI)
        # ex_skill_image.save(temp_name + '_cropped_ex_skill_area.png')
        ex_skill_frame = np.asarray(ex_skill_image)
        ex_skill_frame = cv2.cvtColor(ex_skill_frame, cv2.COLOR_RGB2GRAY)

        # Exスキルの数だけループしてテンプレートマッチング
        for num, template_img in enumerate(BINARY_PRODUCE_EX_SKILLS):
            res = cv2.matchTemplate(ex_skill_frame, template_img, cv2.TM_CCORR_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if (max_val > 0.99):
                # canvas上のExスキルがある位置をクリック
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(canvas, EX_SKILL_SEARCH_LEFT + max_loc[0], EX_SKILL_SEARCH_TOP + max_loc[1])
                actions.click()
                actions.perform()
                break

except KeyboardInterrupt:
    print('処理を中断しました')
    sys.exit(1)