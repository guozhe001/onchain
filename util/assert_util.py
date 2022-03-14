# encoding=utf8
from util.exception import CryptoException


def assert_true(expression, msg):
    if not expression:
        raise CryptoException(msg)
