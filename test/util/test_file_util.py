import json
from pathlib import Path, PurePath
from unittest import TestCase

from config import config_util
from util import file_util


class Test(TestCase):
    def test_write(self):
        file_util.write("temp.cvs", "a,b,c\nc,b,a\n")

    def test_get_last_line(self):
        last_line = file_util.get_last_line(config_util.config_path + "/rinkeby_uniswap_v2_pairs.ini")
        print(last_line)
        split = last_line.split("=")
        pair_info = split[1].strip()
        print(pair_info)
        loads = json.loads(pair_info)
        print(loads)
        print(type(loads))
        print(loads.get("index"))
        print(type(loads.get("index")))

    def test_print_address_length(self):
        print(len("0xfc18d8382697552737921dF830102579f000228D"))
        print(len("0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"))

    def test_file_list_dir1(self):
        current_path = Path(__file__).resolve()
        print(current_path.parent)
        print(type(current_path.parent))

    def test_get_new_name(self):
        # LINA-usdt-kline.csv
        new_name = get_new_name("LINA-usdt-kline.csv")
        # return f"data/{ex}-{coin}-{quote}-{interval.name}.csv"
        self.assertEqual("huobi-LINA-USDT-MIN1.csv", new_name)


def get_new_name(old_name):
    coin = old_name.split("-")[0]
    return f"huobi-{coin}-USDT-MIN1.csv"
