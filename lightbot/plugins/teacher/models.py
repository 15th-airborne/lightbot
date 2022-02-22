import datetime
import random
import re

from peewee import *

from database import database, create_tables, BaseModel


class QuestionAnswer(BaseModel):
    user_id = IntegerField()
    group_id = IntegerField()
    question = CharField()
    answer = CharField()

    teach_time = DateTimeField(default=datetime.datetime.now)
    use_time = DateTimeField(default=datetime.datetime(2000, 1, 1))
    delete = BooleanField(default=False)

    class Meta:
        table_name = "question_answer"
        # constraints = [SQL('UNIQUE (question, answer)')]


def add_question_answer(user_id, group_id, question, answer):
    try:
        # question = get_image_file_name(question)
        # answer = get_image_answer(answer)
        qa = QuestionAnswer.get(question=question, answer=answer)
        if qa.delete == True:
            qa.delete = False
            qa.save()
            return "我学会了！"
        return "我学过了！"
    except QuestionAnswer.DoesNotExist:
        with database.atomic():
            # Attempt to create the user. If the username is taken, due to the
            # unique constraint, the database will raise an IntegrityError.
            QuestionAnswer.create(
                user_id=user_id,
                group_id=group_id,
                question=question,
                answer=answer,
            )
        return "我学会了！"


def get_image_file_name(message):
    """ 聊天信息只有图片时获取图片名 """
    res = re.match("^\[CQ:image,file=(.*?),.*?\]$", message)
    if res:
        image_file_name = res.group(1)
        return image_file_name
    return message


def answer_question(question):
    question = get_image_file_name(question)

    # qas = QuestionAnswer.select().where(QuestionAnswer.question == question).order_by(QuestionAnswer.use_time)
    # query = QuestionAnswer.select().where((QuestionAnswer.question == question) & (not QuestionAnswer.delete))
    
    qa = QuestionAnswer.select()\
        .where(
            QuestionAnswer.question == question,
            QuestionAnswer.delete == False,
        )\
        .order_by(fn.Rand()) \
        .get_or_none()
    
    if qa:
        # qa = random.choice(query)
        # print(qa.answer)
        # 更新使用时间 保证每次都回复不一样的话
        # p = QuestionAnswer. \
        #     update(use_time=datetime.datetime.now()). \
        #     where(QuestionAnswer.id == qa.id)
        # p.execute()
        # [CQ:image,file=52a5384382d152c61f0cbf4e5307961b.image,url=https://gchat.qpic.cn/gchatpic_new/1420125167/565657000-2931184282-52A5384382D152C61F0CBF4E5307961B/0?term=3,subType=0]

        if qa.answer.startswith('[CQ:image'):
            # 将file的值替换成url的值。
            answer = re.sub("^(\[CQ:image,file)(=.*?)(=.*?\])$", r"\1\3", qa.answer)
            return answer

        return qa.answer


def delete_question_answer(question, answer):
    # qa = QuestionAnswer.get_or_none(question=question, answer=answer)
    res = QuestionAnswer.update(delete=True)\
        .where(
            QuestionAnswer.question==question,
            QuestionAnswer.answer==answer,
        ).execute()
    if res:
        return "我学废了！"   
    return "我没学过！"


create_tables([QuestionAnswer])
