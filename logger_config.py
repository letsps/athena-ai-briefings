# logger_config.py

import logging
from logging.handlers import TimedRotatingFileHandler
import sys

# ==============================================================================
# 全局日志配置模块 (Global Logging Configuration)
# ==============================================================================

def setup_logger():
    """
    配置并返回一个全局的logger。
    这个logger会将日志同时输出到控制台和文件中。
    """
    # 1. 获取根logger
    # 我们配置根logger，这样项目中所有通过 logging.getLogger(__name__) 获取的子logger都会继承这个配置
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # 设置最低日志级别

    # 避免重复添加handler，如果已经有handler了，就直接返回
    if logger.hasHandlers():
        return logger

    # 2. 创建一个格式化器 (Formatter)
    # 定义日志的输出格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 3. 创建并配置控制台处理器 (StreamHandler)
    # 用于将日志输出到屏幕
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 4. 创建并配置文件处理器 (TimedRotatingFileHandler)
    # 用于将日志写入文件，并按时间自动轮换
    # 'logs/athena.log': 日志文件路径。请确保'logs'文件夹存在。
    # when='midnight': 每天午夜进行日志轮换
    # interval=1: 每天轮换一次
    # backupCount=30: 保留最近30天的日志文件
    # encoding='utf-8': 使用UTF-8编码，支持中文
    file_handler = TimedRotatingFileHandler(
        filename='logs/athena.log',
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logging.info("日志系统初始化成功，将同时输出到控制台和 'logs/athena.log' 文件。")

    return logger

# 在模块加载时就执行配置，并提供一个全局可用的logger实例
logger = setup_logger()