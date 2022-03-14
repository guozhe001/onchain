# encoding=utf8

# 以太坊网络名称
from enum import Enum


class EthereumNetWorkName:
    # Mainnet (Infura): mainnet
    Mainnet = "mainnet"
    # Ropsten (Infura): ropsten
    Ropsten = "ropsten"
    # Rinkeby(Infura): rinkeby
    Rinkeby = "rinkeby"
    # Goerli(Infura): goerli
    Goerli = "goerli"
    # Kovan(Infura): kovan
    Kovan = "kovan"
    # Binance Smart Chain
    BSCMain = "bsc-main"
    BSCTest = "bsc-test"
    # Ethereum Classic
    ETC = "etc"
    # Fantom Opera
    FtmMain = "ftm-main"
    FtmTest = "ftm-test"


# 以太币单位
class UnitName:
    WEI = "wei"
    ETHER = "ether"
    GWEI = 'gwei'
    # 'wei':          decimal.Decimal('1'),  # noqa: E241
    # 'kwei':         decimal.Decimal('1000'),  # noqa: E241
    # 'babbage':      decimal.Decimal('1000'),  # noqa: E241
    # 'femtoether':   decimal.Decimal('1000'),  # noqa: E241
    # 'mwei':         decimal.Decimal('1000000'),  # noqa: E241
    # 'lovelace':     decimal.Decimal('1000000'),  # noqa: E241
    # 'picoether':    decimal.Decimal('1000000'),  # noqa: E241
    # 'gwei':         decimal.Decimal('1000000000'),  # noqa: E241
    # 'shannon':      decimal.Decimal('1000000000'),  # noqa: E241
    # 'nanoether':    decimal.Decimal('1000000000'),  # noqa: E241
    # 'nano':         decimal.Decimal('1000000000'),  # noqa: E241
    # 'szabo':        decimal.Decimal('1000000000000'),  # noqa: E241
    # 'microether':   decimal.Decimal('1000000000000'),  # noqa: E241
    # 'micro':        decimal.Decimal('1000000000000'),  # noqa: E241
    # 'finney':       decimal.Decimal('1000000000000000'),  # noqa: E241
    # 'milliether':   decimal.Decimal('1000000000000000'),  # noqa: E241
    # 'milli':        decimal.Decimal('1000000000000000'),  # noqa: E241
    # 'ether':        decimal.Decimal('1000000000000000000'),  # noqa: E241
    # 'kether':       decimal.Decimal('1000000000000000000000'),  # noqa: E241
    # 'grand':        decimal.Decimal('1000000000000000000000'),  # noqa: E241
    # 'mether':       decimal.Decimal('1000000000000000000000000'),  # noqa: E241
    # 'gether':       decimal.Decimal('1000000000000000000000000000'),  # noqa: E241
    # 'tether':       decimal.Decimal('1000000000000000000000000000000'),  # noqa: E241


class ContractName:
    UNISWAP_V2_ROUTER = "UNISWAP_V2_ROUTER"
    UNISWAP_V2_FACTORY = "UNISWAP_V2_FACTORY"
    UNISWAP_V2_PAIR = "UNISWAP_V2_PAIR"
    WETH9 = "WETH9"
    UNI = "UNI"
    DAI = "DAI"
    USDT = "USDT"
    # 平台代币地址
    CURRENCY_SYMBOL = "CURRENCY_SYMBOL"
    SUSHI = "SUSHI"
    PANCAKE_SWAP_ROUTER = "PANCAKE_SWAP_ROUTER"
    PANCAKE_SWAP_FACTORY = "PANCAKE_SWAP_FACTORY"
    PANCAKE_SWAP_PAIR = "PANCAKE_SWAP_PAIR"
    WBNB = "WBNB"
    BUSD = "BUSD"
    FOXY = "FOXY"
    RARITY = "RARITY"


class GasStrategy(Enum):
    #  the median gas prices for all transactions currently included in the mining block
    RAPID = "rapid"
    # the gas price transaction "N", the minimum priced tx currently included in the mining block
    FAST = "fast"
    # the gas price of the Max(2N, 500th) transaction in the mempool
    STANDARD = "standard"
    # the gas price of the max(5N, 1000th) transaction within the mempool
    SLOW = "slow"


class EtherScanHost:
    BSC_SCAN = "https://bscscan.com/"
    ETHER_SCAN = "https://etherscan.io/"


class JSONRpc:
    LATEST = "latest"
