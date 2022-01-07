import os

# "/projects/lightbot/lightbot
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CQHTTP_PATH = "/projects/lightbot/cqhttp"
IMAGE_DIR = "/projects/lightbot/img"
CACHE_IMAGE_PATH = "projects/lightbot/cqhttp/data"

DATABASE_PARAMS = {
    "database": "qq_bot",  # 数据库名
    "user": "root",
    "password": "123456",
    "host": "localhost",
    "port": 3306
}


if __name__ == '__main__':
    print(BASE_PATH)
