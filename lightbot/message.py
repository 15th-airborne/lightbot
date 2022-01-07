import asyncio
import os
import re
import random

import aiohttp


class Sender:
    def __init__(self, user_id, nickname, sex, age):
        self.user_id = user_id
        self.nickname = nickname
        self.sex = sex
        self.age = age


def get_cq_code(type_, **kwargs):
    params = ""
    for k, v in kwargs.items():
        params += f",{k}={v}"
    return f"[CQ:{type_}{params}]"


class GroupMessage:
    def __init__(
            self,
            time: int,
            self_id: int,
            post_type: str,
            message_type: str,
            sub_type: str,
            message_id: int,
            group_id: int,
            user_id: int,
            anonymous: dict,
            message: str,
            raw_message: str,
            font: int,
            sender: dict
    ):
        self.time = time
        self.self_id = self_id
        self.post_type = post_type
        self.message_type = message_type
        self.sub_type = sub_type
        self.message_id = message_id
        self.group_id = group_id
        self.user_id = user_id
        self.anonymous = anonymous
        self.message = message
        self.raw_message = raw_message
        self.font = font
        self.sender = Sender(sender)


if __name__ == '__main__':
    # asyncio.run(main())
    pass
