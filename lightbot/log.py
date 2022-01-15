import os
import logging
import logging.handlers
from config import LOG_DIR, LOG_FILE_PATH

# 创建logger记录器
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# 文件处理器，保存日志到文件
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

file_handler = logging.handlers.RotatingFileHandler(
    filename=LOG_FILE_PATH, 
    maxBytes=1024 * 1024,  # 日志最大为1Mb
    backupCount=2,  # 最多备份2个日志
    encoding='utf8'
)

file_handler.setLevel(logging.INFO)

# 输出日志到终端
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# 显示格式
formatter = logging.Formatter(
    fmt="[%(asctime)s][%(levelname)s][%(name)s]:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.debug('日志初始化完毕')
