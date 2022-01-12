import os
import random
import config

from plugin_manager import GroupMessagePlugin, all_plugins
from utils import cq

IMG_DIR = config.IMAGE_DIR
IMG_FILES = os.listdir(IMG_DIR)


class SetuPlugin(GroupMessagePlugin):
    def get_reply(self):
        if 'setu' in self.message or ('色' in self.message and '图' in self.message):
            random_index = random.randint(0, len(IMG_FILES) - 1)
            img_path = os.path.join(IMG_DIR, IMG_FILES[random_index])  # 根据索引获得图片路径
            return cq.image(img_path)


all_plugins.append(SetuPlugin)