import unittest
from unittest import TestCase

from config import config_util
from constant import constant


class Test(TestCase):
    def test_list_keys(self):
        values = config_util.list_keys(config_util.get_section([constant.CONFIG_API, constant.EXCHANGE_OKEX]),
                                       [constant.CONFIG_API_KEY, constant.CONFIG_SECRET,
                                        constant.CONFIG_PASSPHRASE])
        for v in values:
            print(v)


if __name__ == '__main__':
    unittest.main()
