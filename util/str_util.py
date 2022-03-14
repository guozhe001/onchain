# encoding=utf8
import re

from constant import constant

res = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')


def is_blank(s):
    return s is None or s == ""


def contains(text, s):
    """
    检查text是否包含s
    :param text:     需要校验的字符串
    :param s:        可能被包含的字符串
    :return: 如果text中包含s返回True，否则返回False
    """
    return text.find(s) >= 0


def capitalize(string, lower_rest=False):
    """ 首字母大写
    :param string: 传入原始字符串
    :param lower_rest: bool, 控制参数--是否将剩余字母都变为小写
    :return: 改变后的字符
    """
    return string[:1].upper() + (string[1:].lower() if lower_rest else string[1:])


def filter_emoji(s, restr=''):
    # 过滤表情
    return res.sub(restr, s)


def have_emoji(s):
    return res.findall(s)


def to_str(bytes_or_str):
    return bytes_or_str.decode(constant.UTF8) if isinstance(bytes_or_str, bytes) else bytes_or_str


def to_bytes(bytes_or_str):
    return bytes_or_str if isinstance(bytes_or_str, bytes) else bytes_or_str.encode(constant.UTF8)
