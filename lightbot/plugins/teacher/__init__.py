from plugin_manager import add_command_temp
from .models import QuestionAnswer, get_image_file_name, add_question_answer, answer_question


@add_command_temp(keywords=['教小月'])
async def teach(bot, event):
    message = event['message']
    words = message.strip().split()
    if len(words) < 3:
        ans = "格式为：教小月 <句子> <回答> \n例:教小月 你是谁 我是你爹"
        await bot.send_group_msg(event['group_id'], ans)

    question = words[1]
    answer = " ".join(words[2:])
    if len(question) > 512 or len(answer) > 512:
        reply = "句子或问题...太...太长了"
    else:
        question = get_image_file_name(question)
        print(question)
        # question = image_question_process()
        # answer = await image_answer_process(self, answer)
        # 如果answer是图片的话，进行一些处理
        reply = add_question_answer(event['user_id'], event['group_id'], question, answer)
    await bot.send_group_msg(event['group_id'], reply)


