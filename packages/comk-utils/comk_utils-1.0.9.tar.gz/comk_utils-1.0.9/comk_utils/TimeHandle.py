import datetime


def str_to_datetime(time_str, format_str=None):
    """
    字符串转datetime

    :param time_str:
    :param format_str:
    :return:
    """
    if not isinstance(time_str, str):
        raise Exception('time({}) is not str'.format(type(time_str)))
    if not format_str:
        format_str = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.strptime(time_str, format_str)


def datetime_to_str(time, format_str=None):
    """
    datetime转字符串

    :param time:
    :param format_str:
    :return:
    """
    if not isinstance(time, (datetime.datetime, datetime.date)):
        raise Exception('time({}) is not datetime'.format(type(time)))
    if not format_str:
        format_str = '%Y-%m-%d %H:%M:%S'
    return time.strftime(format_str)


def tomorrow_day(day):
    """
    获取明天

    :param day:
    :return:
    """
    if not isinstance(day, (datetime.datetime, datetime.date)):
        raise Exception('day({}) is not datetime'.format(type(day)))
    return day + datetime.timedelta(days=1)


def get_day_number(day):
    """
    获取日期的星期几的数值

    :param day:
    :return:
    """
    if not isinstance(day, (datetime.datetime, datetime.date)):
        raise Exception('day({}) is not datetime'.format(type(day)))
    return int(day.weekday()) + 1


def check_weekend(day):
    """
    判断该日期是否是周末

    :return:
    """
    if not isinstance(day, (datetime.datetime, datetime.date)):
        raise Exception('day({}) is not datetime'.format(type(day)))
    return get_day_number(day) in (6, 7)


def compute_two_times_sub_seconds(time1, time2):
    """
    计算两个时间的时间差的秒数

    :return:
    """
    if isinstance(time1, (datetime.datetime, datetime.date)) and isinstance(time2, (datetime.datetime, datetime.date)):
        return int((time1 - time2).total_seconds())  # 转化为int型数据更好，获取具体的秒数
    else:
        raise Exception('time1({}) and time2({}) is not datetime'.format(type(time1), type(time2)))


def compute_day_last_time():
    """
    计算今天的剩余时间

    :return:
    """
    now = datetime.datetime.now()
    tomorrow = tomorrow_day(now)
    tomorrow_zero_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)  # 获取明天早上0点整
    ex = compute_two_times_sub_seconds(tomorrow_zero_time, now)
    return ex
