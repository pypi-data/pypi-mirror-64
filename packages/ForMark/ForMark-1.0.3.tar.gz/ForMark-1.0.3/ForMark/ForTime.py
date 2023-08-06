"""
时间处理
"""
import time
import datetime

from ForMark.ForException import exception_return_decorator
from ForMark.ForString import is_none_str


@exception_return_decorator(None)
def timestamp_to_time(timestamp) -> datetime.datetime:
    """
    时间戳转时间格式
    :param timestamp: 时间戳
    :return:
    """
    if is_none_str(timestamp):
        return None
    if isinstance(timestamp, datetime.datetime):
        return timestamp
    if isinstance(timestamp, str):
        timestamp = int(timestamp)
    if not isinstance(timestamp, int):
        return None
    if timestamp > 9999999999:
        timestamp = timestamp // 1000
    return datetime.datetime.fromtimestamp(timestamp)


def datetime_to_str(dt, format='%Y-%m-%d %H:%M'):
    if dt:
        return dt.strftime(format)
    else:
        return ''


def get_time_file():
    return time.strftime("%Y/%m/%d/")


if __name__ == '__main__':
    print(timestamp_to_time(1581902524433))
    print(type(timestamp_to_time(1581902524433)))
    print(type(timestamp_to_time(None)))
