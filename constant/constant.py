# encoding=utf8

# config配置相关
from enum import Enum

CONFIG_API = "api"
CONFIG_API_KEY = "api_key"
CONFIG_SECRET = "secret"
CONFIG_SPLIT = "."
CONFIG_WANTED = "wanted"
CONFIG_ACCOUNT_ID = "_account_id"
CONFIG_PASSPHRASE = "passphrase"
CONFIG_ETHEREUM_PROJECT_ID = "ethereum_project_id"
CONFIG_ADDRESS = "address"
CONFIG_ETH_ACCOUNT = "eth_account"
CONFIG_PRIVATE_KEY = "private_key"
CONFIG_TWITTER = "twitter"

# 交易所名称
EXCHANGE_OKEX = "okex"
EXCHANGE_GATE = "gate"
EXCHANGE_HUOBI = "huobi"
EXCHANGE_BINANCE = "binance"
EXCHANGE_COINBASE = "coinbase"
EXCHANGE_MXC = "mxc"
EXCHANGE_UNISWAP_V2 = "uniswap_v2"
EXCHANGE_PANCAKE_SWAP_V2 = "pancake"
EXCHANGE_COINMARKETCAP = "coinmarketcap"

EXCHANGE_ETHERSCAN = "etherscan"
EXCHANGE_BSCSCAN = "bscscan"

# 已经支持的交易所
SUPPORTED_EXCHANGE = [EXCHANGE_OKEX, EXCHANGE_GATE, EXCHANGE_HUOBI, EXCHANGE_MXC]

# 环境
ENV_TEST = "test"
ENV_PRO = "pro"
ENV_CONCURRENT = "concurrent"
ENV_BETA = "beta"

UTF8 = "utf-8"

# ETHEREUM链提供的api
ETHEREUM = [EXCHANGE_ETHERSCAN, EXCHANGE_BSCSCAN]

binance_url = "https://www.binance.com"

# 通知平台-钉钉:https://developers.dingtalk.com/document/robots/custom-robot-access/
NOTIFY_DINGTALK = "dingtalk"
# 通知平台-server酱：https://sct.ftqq.com/
NOTIFY_SERVERCHAN = "serverchan"


class Parenthesis:
    # 中文括号
    chinese_left = "（"
    chinese_right = "）"
    # 英文括号
    english_left = "("
    english_right = ")"


# 默认的报价币种
DEFAULT_QUOTE_CURRENCY = "usdt"

BLANK = ""

COMMA = ","

EMPTY_DICT = {}


class EnvName:
    ETH_NET_WORK = "net_work"
    WEB3_INFURA_PROJECT_ID = "WEB3_INFURA_PROJECT_ID"
    ETHERSCAN_TOKEN = "ETHERSCAN_TOKEN"


class CandlestickIntervalEnum(Enum):
    MIN1 = "1min"
    MIN5 = "5min"
    MIN15 = "15min"
    MIN30 = "30min"
    MIN60 = "60min"
    HOUR4 = "4hour"
    DAY1 = "1day"
    MON1 = "1mon"
    WEEK1 = "1week"
    YEAR1 = "1year"


SECONDS_OF_1MIN = 60
SECONDS_OF_1HOUR = SECONDS_OF_1MIN * 60
SECONDS_OF_1DAY = SECONDS_OF_1HOUR * 24

interval_to_seconds = {
    CandlestickIntervalEnum.MIN1: SECONDS_OF_1MIN,
    CandlestickIntervalEnum.MIN5: SECONDS_OF_1MIN * 5,
    CandlestickIntervalEnum.MIN15: SECONDS_OF_1MIN * 15,
    CandlestickIntervalEnum.MIN30: SECONDS_OF_1MIN * 30,
    CandlestickIntervalEnum.MIN60: SECONDS_OF_1HOUR,
    CandlestickIntervalEnum.HOUR4: SECONDS_OF_1HOUR * 4,
    CandlestickIntervalEnum.DAY1: SECONDS_OF_1DAY,
    # 严格意义上来数，不同月份的间隔是不一样的，此处用到的时候在修改
    CandlestickIntervalEnum.MON1: SECONDS_OF_1DAY * 30,
    CandlestickIntervalEnum.WEEK1: SECONDS_OF_1DAY * 7,
    # 严格意义上来数，不同年份的间隔是不一样的，此处用到的时候在修改
    CandlestickIntervalEnum.YEAR1: SECONDS_OF_1DAY * 365,
}
