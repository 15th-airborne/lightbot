"""
当群友说确实时，响应群友的确实以免冷场
"""
import pypinyin
from plugin_manager import add_command


@add_command
async def send_indeed(bot, event):
    message = event['message']
    pinyin = pypinyin.pinyin(message, style=pypinyin.NORMAL)
    pinyin = [p[0] for p in pinyin]
    pinyin = "".join(pinyin)
    if "queshi" in pinyin:
        await bot.send_group_msg(event['group_id'], "确实")
        return True

    for text in ['确实', '確實', 'indeed', 'たぃかに', '確かに', '確か']:
        if text in message:
            await bot.send_group_msg(event['group_id'], "确实")
            return True

    return False
