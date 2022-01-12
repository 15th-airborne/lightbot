
# import json
# import random
# import re
# import os

# # import yinglish
# import jieba
# from plugin_manager import StartCommand
# from plugin_manager import add_command, PluginManager
# import config


# @add_command
# async def say_yes(bot, event):
#     if "有无" in event.get('message', ''):
#         texts = ['有', '1', '来来来']
#         ans = random.choice(texts)
#         resp = await bot.send_group_msg(event['group_id'], ans)

# def get_hang_message(message):
#     if message.startswith('夯'):
#         area = message[1:]
#         area = check_area(area)
#         if not area:
#             sentences = ['输入国家名，好吗？',
#                          '你夯的这是个啥？',
#                          '我只夯国家',
#                          '我不理解', ]
#             ans = random.choice(sentences)

#         elif area in ['中国', 'china']:
#             sentences = ["喂？110吗？我要举报一个反动分子",
#                          '这你都敢夯',
#                          '别乱搞',
#                         #  '哟？那你很勇哦',
#                          '你是狗']
#             ans = random.choice(sentences)
#         elif area in ['taiwan', '台湾']:
#             sentences = ["你想梧桐？", "中国人不打中国人", "两岸同属一个中国",
#                          "美国是狗", "日本是狗"]
#             ans = random.choice(sentences)

#         else:
#             dmg = random.randint(0, 10000)
#             ans = '夯' + area + "，造成了%s点伤害" % dmg
#     else:
#         sentences = ['别夯了，esim都亡了',
#                      '打哪里，我要打反',
#                      '先给我来点Q5枪再说',
#                      '我支持中国统一',
#                      '打到美的国主义', ]
#         ans = random.choice(sentences)

#     return ans


# @add_command
# async def send_hang(bot, event):
#     message = event['message']
#     if "夯" in message and "淫语" not in message:
#         ans = get_hang_message(message)
#         await bot.send_group_msg(event['group_id'], ans)


# def get_countries():
#     res = set()
#     with open("./data/country.json", "r", encoding="utf8") as f:
#         c = json.load(f)
#         for item in c:
#             res.add(item['en'].lower())
#             res.add(item['cn'])

#     return res


# countries = get_countries()
# def check_area(area):
#     area = area.lower()
#     if area:
#         words = jieba.lcut(area)
#         if len(words) > 0:
#             w = words[0]
#         else:
#             return ""

#         if w in countries:
#             return w
#         else:
#             return ""
#     return ""


# @add_command
# async def praise_someone(bot, event):
#     message = event['message']
#     sender = event['sender']
#     sender_name = sender['card'] if sender['card'] else sender['nickname']

#     if message.startswith('夸') or message.startswith('誇'):
#         if 'CQ' in sender_name:
#             await bot.send_group_msg(event['group_id'], '淦，你的名字好怪哦，不想夸你')
#             return

#         message = message.replace('夸', '')
#         if '+' in message:
#             name, word = message.split('+')
#         else:
#             name = message
#             word = '真帥'

#         if len(name) >= 10:
#             await bot.send_group_msg(event['group_id'], '你是狗，哪有这么长的名字')
#             return

#         if name == '我':
#             name = sender_name

#         if name == '小月':
#             await bot.send_group_msg(event['group_id'], '谢谢~')
#             return

#         await bot.send_group_msg(event['group_id'], name + word)


# @add_command
# async def chs2yin(bot, event):
#     message = event['message']

#     if message.startswith("淫语"):
#         text = message.replace("淫语", "")

#         if text.startswith("骂"):
#             event['message'] = text
#             text = get_curse_text(bot, event)
#             print('curse text', text)
#         elif text.startswith('夯'):
#             text = get_hang_message(text)

#         await bot.send_group_msg(event['group_id'], yinglish.chs2yin(text))


# @add_command
# async def injection(bot, event):
#     message = event['message']
#     if message.startswith("注入"):
#         if "CQ" not in message:
#             sentences = [
#                 '请发带有CQ码的语句',
#                 '来注入，别不注入',
#                 '啊啊啊啊啊啊',
#                 '你故意找猹是吧',
#                 '你注不注吧']
#             ans = random.choice(sentences)
#             await bot.send_group_msg(event['group_id'], ans)
#             return

#         text = message.replace("注入", "")
#         text = text.replace("&#91;", "[")
#         text = text.replace("&#93;", "]")
#         await bot.send_group_msg(event['group_id'], text)
