import datetime
import logging
from concurrent.futures import ThreadPoolExecutor
from logging.config import fileConfig
from threading import Thread

import time

from util.exception import CryptoException

fileConfig('../config/logging_config.ini')

logger = logging.getLogger()


def cycle_and_raise():
    while True:
        try:
            print(f"{Thread.name}, {datetime.datetime.now()}, run....")
            raise CryptoException("异常了！")
        except Exception as e:
            # logger.error(u"获取币安公告和交易异常", exc_info=True)
            logger.exception(e)
        time.sleep(1)


executor = ThreadPoolExecutor()

if __name__ == '__main__':
    executor.submit(cycle_and_raise)
    time.sleep(60)
