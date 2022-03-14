# encoding=utf8
import logging

from constant import ethereum_constant, constant
from evm_chain.dex.erc20_contract import ERC20
from evm_chain.dex.uniswap_v2_contract import MainNetUniswapV2Router, MainNetUniswapV2Factory, UniswapV2Pair, \
    PairSwapEventKey

logger = logging.getLogger(__name__)


def get_account_balance(erc20_token):
    """
    获取默认账户有多少token
    :param erc20_token 想要获取余额的token地址
    :return 默认账户有多少token
    """
    token = ERC20(ethereum_constant.EthereumNetWorkName.Mainnet, constant.BLANK, erc20_token)
    return token.balance_of_default_account(), token.decimals()


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
    return MainNetUniswapV2Router().swap(amount_in, amount_out_min, path, wait_seconds=wait_seconds)


def get_pair(token0, token1) -> str:
    """
    检查是否有交易对
    :param token0:  代币0
    :param token1:  代币1
    :return: pair address if have else None
    """
    return MainNetUniswapV2Factory().get_pair(token0, token1)


def get_price_input(amount0_out, token0, token1):
    """
    如果想要获取amount0_out个token0，需要支付的token1的数量
    :return:
    """
    return MainNetUniswapV2Router().get_amounts_in(amount0_out, token0, token1)


def get_price_out(amount0_in, token0, token1):
    """
    获取如果支付amount0_in个token0，能够得到的token1的数量
    :return:
    """
    return MainNetUniswapV2Router().get_amounts_in(amount0_in, token0, token1)


def get_history_price(pair_address: str, token_address: str, within_blocks: int):
    """
    在指定区块内获取交易对中某个token的历史价格
    :param pair_address:    交易对地址
    :param token_address:   想要获取价格的token地址
    :param within_blocks:   在多少个区块内
    :return:
    """
    pair = UniswapV2Pair(ethereum_constant.EthereumNetWorkName.Mainnet, constant.BLANK, pair_address)
    history_swap_events = get_swap_event(pair, pair.get_height() - within_blocks)
    token0_price = pair.token0() == token_address
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


def get_swap_event(pair: UniswapV2Pair, from_block):
    argument_filters = {PairSwapEventKey.SENDER: MainNetUniswapV2Router().get_address()}
    return pair.get_filter_event("Swap", argument_filters=argument_filters, from_block=from_block)
