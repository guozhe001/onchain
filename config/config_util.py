# encoding=utf8

import configparser
import logging
import os

from constant import constant, ethereum_constant

logger = logging.getLogger(__name__)

# 当测试时打开
os.environ[constant.EnvName.ETH_NET_WORK] = ethereum_constant.EthereumNetWorkName.BSCMain

config_path = os.path.dirname(os.path.abspath(__file__))
logger.info(config_path)
config = configparser.RawConfigParser()

config.read([config_path + "/api_key_config.ini", config_path + "/contract_address.ini"])


def get(section, key):
    return list_all(section).get(key)


def list_keys(section, keys):
    result = []
    for k in keys:
        result.append(get(section, k))
    return result


def list_all(section):
    return config[section]


def list_sections():
    return config.sections()


# 获取指定交易所的apikey和secret
def get_api_key_secret(exchange) -> (str, str):
    section = get_section([constant.CONFIG_API, exchange])
    return list_keys(section, [constant.CONFIG_API_KEY, constant.CONFIG_SECRET])


# 获取指定交易所的apikey和secret
def get_api_key(exchange):
    section = get_section([constant.CONFIG_API, exchange])
    return get(section, constant.CONFIG_API_KEY)


# 根据key获取section
def get_section(key_list):
    return str.join(constant.CONFIG_SPLIT, key_list)


def get_pair_info(address):
    return get("pair", address)
