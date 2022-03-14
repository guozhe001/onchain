# encoding=utf8
import logging

from django.conf import settings

from constant import constant
from constant.ethereum_constant import EthereumNetWorkName
from evm_chain.dex import pancake_swap_contract, erc20_contract, uniswap_v2_contract
from evm_chain.dex.pancake_swap_contract import PancakeSwapPair
from evm_chain.dex.uniswap_v2_contract import MainNetUniswapV2Pair
from evm_chain.models import PairInfo, ERC20Token
from util.exception import CryptoException
from util import str_util, file_util

logger = logging.getLogger(__name__)


def save_token_by_address(network, token_address):
    token0_in_db = ERC20Token.get_by_address(net_work=network, address=token_address)
    if not token0_in_db:
        ec = erc20_contract.ERC20(network, "default", token_address)
        model_token = ERC20Token()
        model_token.address = token_address
        model_token.name = ec.name()
        model_token.symbol = ec.symbol()
        model_token.decimals = ec.decimals()
        model_token.net_work = network
        _save_token(model_token)


def _save_token(model_token: ERC20Token):
    logger.debug(f"_save_token， address={model_token.address}, name={model_token.name}, symbol={model_token.symbol}, "
                 f"decimals={model_token.decimals}, net_work={model_token.net_work}")
    token0_in_db = ERC20Token.get_by_address(net_work=model_token.net_work, address=model_token.address)
    if not token0_in_db:
        model_token.name = model_token.name[:512]
        model_token.save()


def save_pair_and_token(network, pair_address, pair_index, token0_address, token1_address):
    save_pair_info(pair_address, pair_index, token0_address, token1_address, network)
    save_token_by_address(network, token0_address)
    save_token_by_address(network, token1_address)


def get_pairs_and_save(network):
    if network == EthereumNetWorkName.Mainnet:
        factory = uniswap_v2_contract.MainNetUniswapV2Factory()
    elif network == EthereumNetWorkName.BSCMain:
        factory = pancake_swap_contract.PancakeSwapFactory()
    else:
        raise CryptoException(f"不支持的网络：{network}")
    all_pairs_length = factory.all_pairs_length()
    max_index_pair = PairInfo.get_max_index(network)
    max_index = max_index_pair[0].index + 1 if max_index_pair else 0
    logger.info(f"网络{network}已经下载的最大index={max_index}, 目前的最大index={all_pairs_length}")
    for i in range(max_index, int(all_pairs_length)):
        try:
            pair_address = factory.all_pairs(i)
            if network == EthereumNetWorkName.Mainnet:
                pair = MainNetUniswapV2Pair("default", pair_address)
            elif network == EthereumNetWorkName.BSCMain:
                pair = PancakeSwapPair("default", pair_address)
            else:
                raise CryptoException(f"不支持的网络：{network}")
            token0_address = pair.token0()
            token1_address = pair.token1()
            save_pair_and_token(network, pair_address, i, token0_address, token1_address)
        except Exception as e:
            logger.exception(e)


net_map = {
    "pancake": [EthereumNetWorkName.BSCMain, "bsc-main_pancake_swap_pairs.ini"],
    "uni": [EthereumNetWorkName.Mainnet, "mainnet_uniswap_v2_pairs.ini"],
}


def move_pairs(dex_name):
    net = net_map.get(dex_name)[0]
    uni_pairs_file = settings.BASE_DIR.joinpath('config', net_map.get(dex_name)[1])
    pairs_in_file = file_util.read_file(uni_pairs_file)[1:]
    logger.info(f"uni_pairs_file={uni_pairs_file}, pairs_in_file len={len(pairs_in_file)}")
    count = 0
    for pair in pairs_in_file:
        if count % 100 == 0:
            logger.info(f"move_pairs, pair={pair}")
            logger.info(f"move_pairs, count={count}")
        count += 1
        # 防止在其他地方有等号出现,保留第一个等号后面的所有的数据
        split_ = pair[pair.find("=") + 1:]
        pair_address, pair_index, token0_dict, token1_dict = uniswap_v2_contract.str_to_pair_info(split_.strip())
        t0: ERC20Token = dict_to_erc20token(token0_dict)
        t0.net_work = net
        _save_token(t0)
        t1: ERC20Token = dict_to_erc20token(token1_dict)
        t1.net_work = net
        _save_token(t1)
        save_pair_info(pair_address, pair_index, t0.address, t1.address, net)


def dict_to_erc20token(erc20_dict) -> ERC20Token:
    token = ERC20Token()
    token.address = erc20_dict.get("address")
    name = constant.BLANK if erc20_dict.get("name") is None else erc20_dict.get("name")
    token.name = str_util.filter_emoji(name) if str_util.have_emoji(name) else name
    symbol = constant.BLANK if erc20_dict.get("symbol") is None else \
        erc20_dict.get("symbol") if isinstance(erc20_dict.get("symbol"), str) else erc20_dict.get("symbol")[0]
    token.symbol = str_util.filter_emoji(symbol) if str_util.have_emoji(symbol) else symbol
    token.decimals = 0 if erc20_dict.get("decimals") is None else erc20_dict.get("decimals")
    return token


def save_pair_info(pair_address, pair_index, token0_address, token1_address, net):
    pair_in_db = PairInfo.get_by_address(address=pair_address, net_work=net)
    if not pair_in_db:
        p = PairInfo()
        p.address = pair_address
        p.index = pair_index
        p.token0 = token0_address
        p.token1 = token1_address
        p.net_work = net
        p.save()


def save_new_pair_info(network, events):
    """
    保存交易对信息
    :param events:
    :return:
    """
    # AttributeDict({'args': AttributeDict({'token0': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
    #                                       'token1': '0xDab763f32f2D1289F33225cCcE512590D3F18F0d',
    #                                       'pair': '0xa460D56FE86d39cDf522Ee73F26f0E01d84E6ce9',
    #                                       '': 48800}), 'event': 'PairCreated', 'logIndex': 121,
    #                'transactionIndex': 135, 'transactionHash': HexBytes(
    #         '0xf3d9bebc35ece640c749419ecc97aa2ce93c3fbbb3f714a53471ba8f5916c90a'),
    #                'address': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f', 'blockHash': HexBytes(
    #         '0x867a1df6f37db10b78a78bd53866e6a5e52cec929c3d7d99379e56b9840e4475'),
    #                'blockNumber': 12855585})
    for e in events:
        args = e.get("args")
        save_pair_and_token(network, args.get("pair"), args.get("") - 1, args.get("token0"), args.get("token1"))


#
#
# w3_contract_uni_v2_factory = ethereum.web3_contract(
#     address=ethereum.get_contract_address(EthereumNetWorkName.BSCMain, ContractName.PANCAKE_SWAP_FACTORY),
#     abi=ethereum.get_abi(ContractName.PANCAKE_SWAP_FACTORY))
#
#
# def listen_pair_created(network):
#     logger.debug("listen_pair_created ...")
#     ethereum_ins = ethereum.get_ethereum(network)
#     transfer_filter = w3_contract_uni_v2_factory.events.PairCreated.createFilter(fromBlock=ethereum_ins.get_height())
#     """监听uniswap v2的交易对常见事件，一旦有新的交易对创建则通知并记录交易对信息"""
#     while True:
#         entries = transfer_filter.get_new_entries()
#         if entries:
#             save_new_pair_info(network, entries)


def listen_uni_pair_created():
    get_pairs_and_save(EthereumNetWorkName.Mainnet)


def listen_pancake_pair_created():
    get_pairs_and_save(EthereumNetWorkName.BSCMain)
