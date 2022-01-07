import datetime

from peewee import *

import config


# simple utility function to create tables
def create_tables(tables):
    with database:
        database.create_tables(tables)


database = MySQLDatabase(**config.DATABASE_PARAMS)


class BaseModel(Model):
    class Meta:
        database = database


""" 获取群成员列表的返回值
group_id = BigIntegerField()  # 群号
user_id = BigIntegerField()  # QQ 号
nickname = CharField()  # 昵称
card = CharField()  # 群名片／备注
sex = CharField()  # 性别, male 或 female 或 unknown
age = IntegerField()  # 年龄
area = CharField()  # 地区
join_time = IntegerField()  # 加群时间戳
last_sent_time = IntegerField()  # 最后发言时间戳
level = CharField()  # 成员等级
role = CharField()  # 角色, owner 或 admin 或 member
unfriendly = BooleanField()  # 是否不良记录成员
title = CharField()  # 专属头衔
title_expire_time = BigIntegerField()  # 专属头衔过期时间戳
card_changeable = BooleanField()  # 是否允许修改群名片
shut_up_timestamp = BigIntegerField()  # 禁言到期时间  
"""


class User(BaseModel):
    group_id = BigIntegerField()  # 群号
    user_id = BigIntegerField()  # QQ 号
    nickname = CharField()  # 昵称
    card = CharField()  # 群名片／备注
    sex = CharField()  # 性别, male 或 female 或 unknown
    age = IntegerField()  # 年龄
    area = CharField()  # 地区
    join_time = IntegerField()  # 加群时间戳
    last_sent_time = IntegerField()  # 最后发言时间戳
    level = CharField()  # 成员等级
    role = CharField()  # 角色, owner 或 admin 或 member
    unfriendly = BooleanField()  # 是否不良记录成员
    title = CharField()  # 专属头衔
    title_expire_time = BigIntegerField()  # 专属头衔过期时间戳
    card_changeable = BooleanField()  # 是否允许修改群名片
    shut_up_timestamp = BigIntegerField()  # 禁言到期时间

    teach_time = DateTimeField(default=datetime.datetime.now)
    use_time = DateTimeField(default=datetime.datetime(2000, 1, 1))

    class Meta:
        table_name = "user"


class Group(BaseModel):
    group_id = BigIntegerField()  # 群号
    group_name = CharField()  # 群名
    group_memo = CharField()  # 群备注
    group_create_time = BigIntegerField()  # 群创建时间
    group_level = IntegerField()  # 群等级
    member_count = IntegerField()  # 成员数
    max_member_count = IntegerField()  # 最大成员数（群容量）

    class Meta:
        table_name = "group"


def get_object(model, **kwargs):
    # print(user_id, group_id)
    try:
        obj = model.get(**kwargs)
    except model.DoesNotExist:
        obj = model.create(**kwargs)
    return obj
