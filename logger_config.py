# logger_config.py (Version 1.2 - Refined Comments Final Edition)

import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import os

# ==============================================================================
# "雅典娜"项目全局日志配置中心
#
# 通过在项目启动时最先导入此模块，确保所有后续模块共享同一个、
# 经过完整配置的logger实例。
# ==============================================================================

def setup_logger():
    """
    配置并返回一个全局的根logger实例。
    该函数会自动检查并创建日志目录，并设置日志同时输出到控制台和文件。
    """
    LOG_DIR = "logs"
    LOG_FILE = os.path.join(LOG_DIR, "athena.log")

    # 核心健壮性设计：确保日志目录存在。
    # 这是为了让项目在被克隆到一个新环境后，首次运行时能自动创建所需目录。
    if not os.path.exists(LOG_DIR):
        print(f"INFO: 日志目录 '{LOG_DIR}' 不存在，正在创建...")
        try:
            os.makedirs(LOG_DIR)
        except OSError as e:
            print(f"FATAL: 无法创建日志目录 '{LOG_DIR}'. 错误原因: {e}")
            sys.exit(1)
            
    # 获取根logger，以便所有子模块的logger都能继承此配置。
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 防止因重复导入而多次添加handler，导致日志重复输出。
    if logger.hasHandlers():
        return logger

    # 定义统一的日志格式。
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # --- 配置控制台输出 ---
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # --- 配置文件输出，并实现按日轮换 ---
    # TimedRotatingFileHandler能够自动管理日志文件，防止单个文件无限增大。
    file_handler = TimedRotatingFileHandler(
        filename=LOG_FILE,
        when='midnight',    # 每天午夜进行日志分割
        backupCount=30,     # 最多保留30天的日志备份
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    logger.info(f"日志系统初始化成功，输出至控制台和 '{LOG_FILE}'。")

    return logger

# 在模块导入时立即执行配置，生成全局唯一的logger实例。
logger = setup_logger()