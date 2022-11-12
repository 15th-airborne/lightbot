
from plugin_manager import add_command


@add_command('测试')
async def demo(bot, event):
    await bot.send_group_msg(542423773, '测试')