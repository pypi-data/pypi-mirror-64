import os
from loguru import logger
"""
日志
"""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(BASE_DIR, 'log/bb.log')
logger.add(log_file_path, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", filter="", level="INFO")


def logger_info(*msg):
    logger.info(msg)


def show(*msg):
    logger.info(msg)


def logger_error(*msg):
    logger.error(msg)


if __name__ == '__main__':
    logger_info("33", "44")
