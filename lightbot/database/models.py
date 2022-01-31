import datetime

from peewee import *

import config
import logging
logger = logging.getLogger(__name__)

# simple utility function to create tables
def create_tables(tables):
    with database:
        database.create_tables(tables)


database = MySQLDatabase(**config.DATABASE_PARAMS)


class BaseModel(Model):
    class Meta:
        database = database

    @classmethod
    def get_obj(cls, **kwargs):
        try:
            obj = cls.get(**kwargs)
        except cls.DoesNotExist:
            # obj = model.create(**kwargs)
            return
        return obj

# https://docs.go-cqhttp.org/api/#获取群成员列表
class GroupMember(BaseModel):
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

    class Meta:
        table_name = "group_member"

# https://docs.go-cqhttp.org/api/#获取群列表
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
        # obj = model.create(**kwargs)
        return
    return obj


# 公共变量数据库
class PublicVariable(BaseModel):
    user_id = BigIntegerField()
    group_id = BigIntegerField()

    name = CharField()  # 变量名
    value = FloatField()  # 变量值
    c_time = TimestampField()  # 修改时间

    @classmethod
    def get_obj(cls, user_id, group_id, name):
        try:
            obj = cls.get(user_id=user_id, group_id=group_id, name=name)
        except cls.DoesNotExist:
            obj = cls.create(user_id=user_id, group_id=group_id, name=name, value=0)
        return obj

create_tables([Group, GroupMember, PublicVariable])