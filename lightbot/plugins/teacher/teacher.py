from plugin_manager import GroupMessagePlugin
from .models import get_image_file_name, add_question_answer, answer_question
import logging
logger = logging.getLogger(__name__)


class TeachPlugin(GroupMessagePlugin):
    def get_reply(self):
        if not self.message.startswith('教小月'):
            return

        words = self.message.strip().split()
        if len(words) < 3:
            return "格式为：教小月 <句子> <回答> \n例:教小月 你是谁 我是你爹"

        question = words[1]
        answer = " ".join(words[2:])
        if len(question) > 512 or len(answer) > 512:
            return "句子或问题...太...太长了"
        else:
            question = get_image_file_name(question)
            logger.info(question)
            # 如果answer是图片的话，进行一些处理
            reply = add_question_answer(self.user_id, self.group_id, question, answer)
            return reply


class AskPlugin(GroupMessagePlugin):
    def get_reply(self):
        answer = answer_question(self.message)
        return answer

