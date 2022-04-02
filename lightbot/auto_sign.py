# 每天自动签到
import random
from plugins.battle.models import Player


for player in Player.select():
    gold_add = random.randint(50, 150)
    player.sign(gold_add)

# /opt/miniconda3/envs/lightbot/bin/python /projects/lightbot/lightbot/auto_sign.py