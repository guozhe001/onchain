# encoding=utf8
import logging

from constant import constant
from evm_chain.dex import ethereum
from evm_chain.dex.erc20_contract import ERC20
from evm_chain.dex.pancake_swap_contract import *
from evm_chain.dex.uniswap_v2_contract import PairSwapEventKey

logger = logging.getLogger(__name__)

network = EthereumNetWorkName.BSCMain
router = PancakeSwapRouter(network)
factory = PancakeSwapFactory()


def erc20_token(erc20_token_address):
    return ERC20(network, constant.BLANK, erc20_token_address)


def get_account_balance(erc20_token_address):
    """
    获取默认账户有多少token
    :param erc20_token_address 想要获取余额的token地址
    :return 默认账户有多少token
    """
    return erc20_token(erc20_token_address).balance_of_default_account()


def get_address_balance(erc20_token_address, address):
    """
    获取指定地址有多少token
    :param erc20_token_address 想要获取余额的token地址
    :param address             想要获取余额的地址
    :return 默认账户有多少token
    """
    token = erc20_token(erc20_token_address)
    return token.balance_of(address), token.decimals()


def swap(address_in, address_out, amount_in, amount_out_min, wait_seconds):
    """
    兑换
    :param address_in:        支出的token
    :param address_out:       想要的token
    :param amount_in:         支出的token的金额
    :param amount_out_min:    期待的最少兑换的金额，如果无法兑换出这么多则抛异常
    :param wait_seconds:      等待时长，单位秒
    :return:
    """
    path = [address_in, address_out]
    return router.swap(amount_in, amount_out_min, path, wait_seconds=wait_seconds)


def get_pair(token0, token1) -> str:
    """
    检查是否有交易对
    :param token0:  代币0
    :param token1:  代币1
    :return: pair address if have else None
    """
    return factory.get_pair(token0, token1)


def get_price_input(amount0_out, token0, token1):
    """
    如果想要获取amount0_out个token0，需要支付的token1的数量
    :return:
    """
    return router.get_amounts_in(amount0_out, token0, token1)


def get_price_out(amount0_in, token0, token1):
    """
    获取如果支付amount0_in个token0，能够得到的token1的数量
    :return:
    """
    return router.get_amounts_out(amount0_in, token0, token1)


def get_history_price(pair_address: str, token0_address: str, token_address: str, within_blocks: int):
    """
    :param pair_address:   交易对的地址
    :param token0_address: 交易对的token0地址
    :param token_address:  交易对中需要获取价格的地址
    :param within_blocks:  最多不能超过5000
    :return: 按照时间的正序排序的价格列表
    """
    pair_contract = PancakeSwapPair(constant.BLANK, pair_address)
    history_swap_events = get_swap_event(pair_contract, pair_contract.get_height() - within_blocks)
    token0_price = token0_address == token_address
    prices = []
    for e in history_swap_events:
        args = e.get("args")
        amount0_in = args.amount0In
        amount1_in = args.amount1In
        amount0_out = args.amount0Out
        amount1_out = args.amount1Out
        if token0_price:
            if amount0_in and amount1_out:
                prices.append(amount1_out / amount0_in)
            else:
                prices.append(amount1_in / amount0_out)
        else:
            if amount0_in and amount1_out:
                prices.append(amount0_in / amount1_out)
            else:
                prices.append(amount0_out / amount1_in)
        logger.info(
            f"amount0_in={amount0_in}, amount1_in={amount1_in}, amount0_out={amount0_out}, amount1_out={amount1_out}")

    return prices


def get_swap_event(pair: PancakeSwapPair, from_block):
    argument_filters = {PairSwapEventKey.SENDER: PancakeSwapRouter(pair.get_network()).get_address()}
    return pair.get_swap_event(argument_filters=argument_filters, from_block=from_block)


def get_avg_price(prices):
    """
    获取平均价格
    :param prices: 价格列表
    :return: 价格列表的平均价格
    """
    return sum(prices) / len(prices)


def allowance(address):
    return erc20_token(address).allowance(ethereum.default_account.address, router.get_address())


def approve(address):
    erc20_token(address).approve_max(router.get_address())
