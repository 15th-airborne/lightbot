import os
import random
import config

from plugin_manager import add_command
from utils import cq

img_dir = config.IMAGE_DIR
img_files = os.listdir(img_dir)


@add_command
async def send_setu(bot, event):
    message = event['message']
    if 'setu' in message or ('色' in message and '图' in message):
        random_index = random.randint(0, len(img_files) - 1)
        img_path = os.path.join(config.IMAGE_DIR, img_files[random_index])  # 根据索引获得图片路径

        reply_msg = cq.image(img_path)

        await bot.send_group_msg(event['group_id'], reply_msg)  # 发送图片
