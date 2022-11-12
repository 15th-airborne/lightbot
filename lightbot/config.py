import os

# "/projects/lightbot/lightbot
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# 日志模块
LOG_DIR = os.path.join(BASE_PATH, 'logs')
LOG_FILE_PATH = os.path.join(LOG_DIR, 'output.log')

CQHTTP_PATH = "/projects/lightbot/cqhttp"
IMAGE_DIR = "/projects/lightbot/img"
CACHE_IMAGE_PATH = "projects/lightbot/cqhttp/data"

DATABASE_PARAMS = {
    "database": "qq_bot",  # 数据库名
    "user": "root",
    "password": "!Light2077",
    "host": "localhost",
    "port": 3306
}

QQ = 323566263
TEST_GROUP_ID = 542423773

if __name__ == '__main__':
    print(BASE_PATH)
