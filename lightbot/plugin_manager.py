"""
插件管理，实现编写类并放到指定文件目录下就能加载插件的功能

"""


class PluginManager:
    commands = dict()
    keywords = dict()

    @classmethod
    def add_command_temp(cls, keywords):
        """ 试运行 """
        def outer(func):
            for kw in keywords:
                # if kw in cls.keywords:
                #     print("warning")
                cls.keywords[kw] = func

            async def deco(*args, **kwargs):
                res = await func(*args, **kwargs)
                return res
            return deco
        return outer

    @classmethod
    def add_command(cls, func):
        cls.commands[func.__name__] = func

        async def deco(*args, **kwargs):
            res = await func(*args, **kwargs)
            return res

        return deco


class BaseCommand:
    def check(self, *args, **kwargs):
        """ 检查bot的事件有没有触发该命令 """
        raise NotImplemented

    def help(self):
        """ 这个命令的使用方式 """
        raise NotImplemented

    def run(self, bot, event):
        raise NotImplemented


class StartCommand(BaseCommand):
    """ 行首匹配命令，对于出现在行首的字符串进行匹配 """
    keyword = None
    alias = None

    # def __init__(self, bot, event, keyword, alias=None):
    def __init__(self):
        # self.bot = bot  # 触发命令的机器人
        # self.event = event  # 触发命令的事件
        if self.keyword is None:
            raise ValueError('必须定义类变量keyword')

    def check(self, event):
        message = event['message']
        """ 是否触发命令 """
        if message.startswith(self.keyword):
            return True
        elif self.alias:
            for k in self.alias:
                if message.startswith(k):
                    return True
        return False


# for command in commands:
#     if command.check():
#         command.run()
#         break


add_command = PluginManager.add_command
add_command_temp = PluginManager.add_command_temp
