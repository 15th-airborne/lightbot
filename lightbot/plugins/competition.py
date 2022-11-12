from http.client import CannotSendHeader
from plugin_manager import all_private_plugins, PrivateMessagePlugin
from database import database, create_tables, BaseModel
import random
from peewee import *
import datetime
import pandas as pd
# class DemoPrivateMessagePlugin(PrivateMessagePlugin):
#     def get_reply(self):
#         return 'hello'

# all_private_plugins.append(DemoPrivateMessagePlugin)
# 比赛结果
result = {'410421579': {'user_id': '410421579',
  'nickname': 'ylxdzsw',
  'group_a': '50',
  'group_b': '49',
  'group_c': '1',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '30',
  '负': '28',
  '平': '14',
  '总分': '104',
  '排名': '15'},
 '435786117': {'user_id': '435786117',
  'nickname': '梦见月球的猫',
  'group_a': '4',
  'group_b': '51',
  'group_c': '45',
  'create_time': '28/8/2022 17:52:21',
  'update_time': '28/8/2022 17:52:21',
  '胜': '37',
  '负': '34',
  '平': '1',
  '总分': '112',
  '排名': '8'},
 '448246588': {'user_id': '448246588',
  'nickname': 'moyan',
  'group_a': '1',
  'group_b': '1',
  'group_c': '98',
  'create_time': '28/8/2022 17:54:29',
  'update_time': '28/8/2022 17:54:29',
  '胜': '23',
  '负': '43',
  '平': '6',
  '总分': '75',
  '排名': '24'},
 '466353494': {'user_id': '466353494',
  'nickname': '锶氚钴铑鰇镓钌碘碳XIV世',
  'group_a': '49',
  'group_b': '2',
  'group_c': '49',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '36',
  '负': '32',
  '平': '4',
  '总分': '112',
  '排名': '8'},
 '471002006': {'user_id': '471002006',
  'nickname': '半岛铁盒',
  'group_a': '1',
  'group_b': '49',
  'group_c': '50',
  'create_time': '28/8/2022 22:48:02',
  'update_time': '28/8/2022 22:48:04',
  '胜': '30',
  '负': '32',
  '平': '10',
  '总分': '100',
  '排名': '18'},
 '498358698': {'user_id': '498358698',
  'nickname': '丘山金夕嘴',
  'group_a': '35',
  'group_b': '1',
  'group_c': '64',
  'create_time': '28/8/2022 22:46:22',
  'update_time': '28/8/2022 22:46:25',
  '胜': '32',
  '负': '38',
  '平': '2',
  '总分': '98',
  '排名': '20'},
 '502840647': {'user_id': '502840647',
  'nickname': '纯粹感性批判',
  'group_a': '40',
  'group_b': '59',
  'group_c': '1',
  'create_time': '28/8/2022 22:51:10',
  'update_time': '28/8/2022 22:51:12',
  '胜': '34',
  '负': '30',
  '平': '8',
  '总分': '110',
  '排名': '12'},
 '542231415': {'user_id': '542231415',
  'nickname': '嘟嘟嘟嘟',
  'group_a': '50',
  'group_b': '49',
  'group_c': '1',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '30',
  '负': '28',
  '平': '14',
  '总分': '104',
  '排名': '15'},
 '592261707': {'user_id': '592261707',
  'nickname': '魂安故乡',
  'group_a': '42',
  'group_b': '57',
  'group_c': '1',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '36',
  '负': '31',
  '平': '5',
  '总分': '113',
  '排名': '7'},
 '609706115': {'user_id': '609706115',
  'nickname': 'Re 689',
  'group_a': '50',
  'group_b': '32',
  'group_c': '18',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '36',
  '负': '32',
  '平': '4',
  '总分': '112',
  '排名': '8'},
 '617350587': {'user_id': '617350587',
  'nickname': 'jianke',
  'group_a': '1',
  'group_b': '1',
  'group_c': '98',
  'create_time': '28/8/2022 22:43:59',
  'update_time': '28/8/2022 22:44:02',
  '胜': '23',
  '负': '43',
  '平': '6',
  '总分': '75',
  '排名': '24'},
 '649309762': {'user_id': '649309762',
  'nickname': '秋人P',
  'group_a': '3',
  'group_b': '51',
  'group_c': '46',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '37',
  '负': '34',
  '平': '1',
  '总分': '112',
  '排名': '8'},
 '774971443': {'user_id': '774971443',
  'nickname': '非人哉',
  'group_a': '33',
  'group_b': '34',
  'group_c': '33',
  'create_time': '28/8/2022 22:58:12',
  'update_time': '28/8/2022 22:58:15',
  '胜': '30',
  '负': '39',
  '平': '3',
  '总分': '93',
  '排名': '21'},
 '784446480': {'user_id': '784446480',
  'nickname': 'Rice Shower',
  'group_a': '51',
  'group_b': '2',
  'group_c': '47',
  'create_time': '28/8/2022 23:45:45',
  'update_time': '28/8/2022 23:45:47',
  '胜': '41',
  '负': '28',
  '平': '3',
  '总分': '126',
  '排名': '1'},
 '872768758': {'user_id': '872768758',
  'nickname': '工藤新一',
  'group_a': '49',
  'group_b': '49',
  'group_c': '2',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '34',
  '负': '32',
  '平': '6',
  '总分': '108',
  '排名': '14'},
 '897745331': {'user_id': '897745331',
  'nickname': 'yuanyuan',
  'group_a': '50',
  'group_b': '2',
  'group_c': '48',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '37',
  '负': '28',
  '平': '7',
  '总分': '118',
  '排名': '2'},
 '962735942': {'user_id': '962735942',
  'nickname': 'MC_GZSHS',
  'group_a': '85',
  'group_b': '10',
  'group_c': '5',
  'create_time': '28/8/2022 22:44:41',
  'update_time': '28/8/2022 22:44:45',
  '胜': '38',
  '负': '33',
  '平': '1',
  '总分': '115',
  '排名': '5'},
 '996001662': {'user_id': '996001662',
  'nickname': '泥咚森',
  'group_a': '50',
  'group_b': '49',
  'group_c': '1',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '30',
  '负': '28',
  '平': '14',
  '总分': '104',
  '排名': '15'},
 '1129504899': {'user_id': '1129504899',
  'nickname': '新语晨香',
  'group_a': '1',
  'group_b': '49',
  'group_c': '50',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '30',
  '负': '32',
  '平': '10',
  '总分': '100',
  '排名': '18'},
 '1158153804': {'user_id': '1158153804',
  'nickname': '梨花',
  'group_a': '40',
  'group_b': '59',
  'group_c': '1',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '34',
  '负': '30',
  '平': '8',
  '总分': '110',
  '排名': '12'},
 '1420125167': {'user_id': '1420125167',
  'nickname': '•́ωก',
  'group_a': '10',
  'group_b': '80',
  'group_c': '10',
  'create_time': '28/8/2022 17:54:29',
  'update_time': '28/8/2022 17:54:29',
  '胜': '39',
  '负': '33',
  '平': '0',
  '总分': '117',
  '排名': '3'},
 '1434469194': {'user_id': '1434469194',
  'nickname': '喵下士',
  'group_a': '33',
  'group_b': '34',
  'group_c': '33',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '30',
  '负': '39',
  '平': '3',
  '总分': '93',
  '排名': '21'},
 '2488658940': {'user_id': '2488658940',
  'nickname': '柚子ち',
  'group_a': '24',
  'group_b': '52',
  'group_c': '24',
  'create_time': '28/8/2022 22:59:51',
  'update_time': '28/8/2022 22:59:54',
  '胜': '38',
  '负': '34',
  '平': '0',
  '总分': '114',
  '排名': '6'},
 '2590766963': {'user_id': '2590766963',
  'nickname': '六',
  'group_a': '40',
  'group_b': '10',
  'group_c': '50',
  'create_time': '28/8/2022 18:23:12',
  'update_time': '28/8/2022 18:23:12',
  '胜': '37',
  '负': '30',
  '平': '5',
  '总分': '116',
  '排名': '4'},
 '2592363260': {'user_id': '2592363260',
  'nickname': '錬金術師LV6',
  'group_a': '2',
  'group_b': '2',
  'group_c': '96',
  'create_time': '28/8/2022 22:43:15',
  'update_time': '28/8/2022 22:43:19',
  '胜': '29',
  '负': '40',
  '平': '3',
  '总分': '90',
  '排名': '23'}}

result = pd.DataFrame(result)


def get_result(user_id, result):
    res = result.get(str(user_id))
    total = len(result)
    rank = int(res['排名'])
    add_str = ''
    
    if rank == 1:
        add_str = '\n太太太NB辣！！！您就是本届大赛的冠军军！！！小月表示五体投地！！！'
    elif rank == 2:
        add_str = '\n太太NB辣！！您就是本届大赛的亚军！！小月觉得你很棒！！'
    elif rank == 3:
        add_str = '\n太NB辣！您就是本届大赛的季军！小月表示佩服！'
    elif rank <= 5:
        add_str = '\n太厉害了吧，你就是五强的天命之子！'
    elif rank <= 10:
        add_str = '\n牛逼！恭喜您获得本届大赛十强荣誉！'
    elif rank <= 100:
        add_str = '\n厉害！恭喜您获得本届大赛百强荣誉！'
    return (
        f"你的士兵安排为:{res['group_a']}-{res['group_b']}-{res['group_c']}\n"
        f"胜/平/负: {res['胜']}/{res['平']}/{res['负']}\n"
        f"总分：{res['总分']}\n"
        f"排名：{res['排名']}/{total}"
        f"{add_str}"
    )


class SoldierGame(BaseModel):
    user_id = BigIntegerField(primary_key=True)
    nickname = CharField()
    group_a = IntegerField()
    group_b = IntegerField()
    group_c = IntegerField()

    create_time = DateTimeField(default=datetime.datetime.now())
    update_time = DateTimeField(default=datetime.datetime.now())


class SoldierGamePlugin(PrivateMessagePlugin):
    def get_reply(self):
        if not self.message.startswith("士兵博弈"):
            return 

        params = self.message.strip().split()
        if len(params) != 4:
            return '输入不合法'

        numbers = []
        for n in params[1:]:
            if not self.is_correct_number(n):
                return '数字不合法'
            
            n = int(n)
            if n <= 0:
                return '每组至少有1个士兵，且不能为负数！'
            numbers.append(n)
        if sum(numbers) != 100:
            return '三组士兵加和必须为100！'
        
        

        with database.atomic() as transaction:
            try:
                SoldierGame.create(
                    user_id=self.user_id, 
                    nickname=self.username,
                    group_a=numbers[0],
                    group_b=numbers[1],
                    group_c=numbers[2],
                )
                return '游戏报名成功！'
            except:
                if datetime.datetime.now() < datetime.datetime(2022, 9, 1):
                    (SoldierGame
                    .insert(
                        user_id=self.user_id, 
                        nickname=self.username,
                        group_a=numbers[0],
                        group_b=numbers[1],
                        group_c=numbers[2],
                    ).on_conflict(
                        preserve=[
                            SoldierGame.group_a, 
                            SoldierGame.group_b, 
                            SoldierGame.group_c]
                        )
                    .execute())
                    return '策略修改成功！'
                else:
                    return '你已经报过名了！'


    def is_correct_number(self, n: str):
        if not n.isnumeric():
            return False
        return True




class SoldierGameResultPlugin(PrivateMessagePlugin):
    def get_reply(self):
        if not self.message.startswith("比赛结果"):
            return 

        return get_result(self.user_id, result)



create_tables([SoldierGame])
all_private_plugins.append(SoldierGamePlugin)
all_private_plugins.append(SoldierGameResultPlugin)