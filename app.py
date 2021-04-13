# -*- coding: utf-8 -*-
import sys
import click
from datetime import datetime
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
from selenium.webdriver.common.action_chains import ActionChains
import logging
import logzero
from logzero import logger
from commons import *

@click.command()
@click.option('--target', required=True, help="プロデュースとサポート。どっちのExスキルを外すか", type=click.Choice(CARD_TYPE_TARGET_NAMES, case_sensitive=True))
@click.option('--debug', help="デバッグフラグ。trueのときテンプレートマッチングに使用する画像をtempディレクトリに保存します", is_flag=True)
def main(target, debug):

    if debug:
        logzero.loglevel(logging.DEBUG)
    logger.debug('ターゲット:{0}'.format(target))
    ex_skills = BINARY_PRODUCE_EX_SKILLS if target == 'produce' else BINARY_SUPPORT_EX_SKILLS

    check_chrome_started()

    driver = get_started_chrome()
    driver.get("https://shinycolors.enza.fun/exSkill")

    try:
        canvas = driver.find_element_by_tag_name('canvas')

        # Exスキル画面のプロデュースボタンが見えるまで無限ループ
        while True:
            original_image = canvas.screenshot_as_png
            original_image = Image.open(BytesIO(original_image))
            produce_button_image = original_image.crop(PRODUCE_SEARCH_ROI)
            produce_button_frame = np.asarray(produce_button_image)
            produce_button_frame = cv2.cvtColor(produce_button_frame, cv2.COLOR_RGB2BGR)
            res = cv2.matchTemplate(produce_button_frame, BINARY_PRODUCE_ON_BUTTON, cv2.TM_CCORR_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if (max_val > 0.99):
                break

        # Exスキルを外す対象がサポートの場合はここでサポートボタンをクリック
        if target == 'support':
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(canvas, SUPPORT_BUTTON_CLICK_LEFT, SUPPORT_BUTTON_CLICK_TOP).click()
            actions.perform()

        nothing_count = 0
        while True:
            if debug:
                temp_name = TEMP_DIR + datetime.now().strftime("%Y%m%d%H%M%S")
            original_image = canvas.screenshot_as_png
            if debug:
                with open(temp_name + '_org.png', 'wb') as f:
                    f.write(original_image)
            original_image = Image.open(BytesIO(original_image))

            # Exスキルの1～3枠×4列分くらいの領域を切り抜いた画像を作成
            ex_skill_image = original_image.crop(EX_SKILL_SEARCH_ROI)
            if debug:
                ex_skill_image.save(temp_name + '_cropped_ex_skill_area.png')
            ex_skill_frame = np.asarray(ex_skill_image)
            ex_skill_frame = cv2.cvtColor(ex_skill_frame, cv2.COLOR_RGB2GRAY)

            # Exスキルの数だけループしてテンプレートマッチング
            for num, template_img in enumerate(ex_skills):
                res = cv2.matchTemplate(ex_skill_frame, template_img, cv2.TM_CCORR_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if (max_val > 0.99):
                    nothing_count = 0
                    logger.debug(max_val, max_loc)
                    actions = ActionChains(driver)
                    # Exスキルがある位置をクリック
                    actions.move_to_element_with_offset(canvas, EX_SKILL_SEARCH_ROI[0] + max_loc[0], EX_SKILL_SEARCH_ROI[1] + max_loc[1]).click()
                    # はずすボタンをクリック
                    actions.move_to_element_with_offset(canvas, EJECT_BUTTON_CLICK_LEFT, EJECT_BUTTON_CLICK_TOP).click()
                    actions.perform()
                    break
            else:
                if nothing_count == 3:
                    logger.info('Exスキルが3回連続で見つからなかったため下にスクロールします')
                    wheel_element(canvas, 120, 500, 400)
                elif nothing_count >= 8:
                    logger.info('Exスキルが8回連続で見つからなかったため処理を終了します')
                    sys.exit(1)
                nothing_count += 1


    except KeyboardInterrupt:
        logger.info('処理を中断しました')
        sys.exit(1)

if __name__ == '__main__':
    main()