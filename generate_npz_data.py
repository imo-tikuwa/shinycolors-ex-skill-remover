import numpy
import os
import cv2
from datetime import datetime
import glob

RESOURCES_DIR = os.getcwd() + os.sep + 'resources' + os.sep
PRODUCE_EX_SKILL_DIR = RESOURCES_DIR + 'ex_skills' + os.sep + 'produce' + os.sep
SUPPORT_EX_SKILL_DIR = RESOURCES_DIR + 'ex_skills' + os.sep + 'support' + os.sep
EJECT_BUTTON_DIR = RESOURCES_DIR + 'eject_buttons' + os.sep
NPZ_FILE = RESOURCES_DIR + 'bundle.npz'

# Exスキル(プロデュース)のサンプルデータ
BINARY_PRODUCE_EX_SKILLS = []
for image_path in glob.glob(PRODUCE_EX_SKILL_DIR + '*.png'):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    BINARY_PRODUCE_EX_SKILLS.append(image)

# Exスキル(サポート)のサンプルデータ
BINARY_SUPPORT_EX_SKILLS = []
for image_path in glob.glob(SUPPORT_EX_SKILL_DIR + '*.png'):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    BINARY_SUPPORT_EX_SKILLS.append(image)

# 「はずす」ボタンのサンプルデータ
BINARY_EJECT_BUTTONS = []
for image_path in glob.glob(EJECT_BUTTON_DIR + '*.png'):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    BINARY_EJECT_BUTTONS.append(image)


# npz保存
numpy.savez_compressed(NPZ_FILE,
            produce_ex_skills = BINARY_PRODUCE_EX_SKILLS,
            support_ex_skills = BINARY_SUPPORT_EX_SKILLS,
            eject_buttons = BINARY_EJECT_BUTTONS,
            )
print('resouces以下のサンプルデータを元にbundle.npzを作成しました')
