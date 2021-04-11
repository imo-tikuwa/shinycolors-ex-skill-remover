# -*- coding: utf-8 -*-
import sys
import os
import click
import psutil
import time
from datetime import datetime
from PIL import Image
from io import BytesIO
from commons import *

# Exスキル画面を開いた状態で実行する

@click.command()
@click.option('--name', required = True, help = "画像名", type = click.Choice(CARD_TYPE_BUTTON_NAMES, case_sensitive = True))
def main(name):

    check_chrome_started()

    driver = get_started_chrome()

    canvas = driver.find_element_by_tag_name('canvas')
    # 「プロデュース」ボタンをキャプチャ
    image = Image.open(BytesIO(canvas.screenshot_as_png))
    image = image.crop(PRODUCE_BUTTON_ROI)
    image.save(CARD_TYPE_BUTTON_DIR + name + '.png')
    print(name + 'のサンプル画像を保存しました。意図した保存が行えてるか確認してください。')


if __name__ == '__main__':
    main()