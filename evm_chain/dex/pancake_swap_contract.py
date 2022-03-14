# encoding=utf8
import eth_utils

from constant.ethereum_constant import *
from evm_chain.dex import ethereum
from evm_chain.dex.uniswap_v2_contract import UniswapV2FactoryInterface, UniswapV2PairInterface, \
    UniswapV2RouterInterface
from util.singleton import singleton


class PancakeSwapRouter(UniswapV2RouterInterface):
    def __init__(self, network):
        super().__init__(network, ContractName.PANCAKE_SWAP_ROUTER,
                         ethereum.get_contract_address(network, ContractName.PANCAKE_SWAP_ROUTER))

    def swap(self, amount_in, amount_out_min, path, wait_seconds):
        """
        代币之间swap,收款人是当前账户
        :return:
        """
        return self.swap_exact_tokens_for_tokens_with_gas(eth_utils.to_wei(5, UnitName.GWEI), amount_in, amount_out_min,
                                                          path, ethereum.default_account.address,
                                                          wait_seconds)

    def swap_exact_tokens_for_tokens(self, amount_in, amount_out_min, path, to, wait_seconds):
        return self.swap_exact_tokens_for_tokens_with_gas(eth_utils.to_wei(5, UnitName.GWEI), amount_in,
                                                          amount_out_min, path, to, wait_seconds)


@singleton
class BSCMainPancakeSwapRouter(PancakeSwapRouter):
    def __init__(self):
        super().__init__(EthereumNetWorkName.BSCMain)


@singleton
class BSCTestPancakeSwapRouter(PancakeSwapRouter):
    def __init__(self):
        super().__init__(EthereumNetWorkName.BSCTest)


@singleton
class PancakeSwapFactory(UniswapV2FactoryInterface):
    def __init__(self):
        super().__init__(EthereumNetWorkName.BSCMain, ContractName.PANCAKE_SWAP_FACTORY)


@singleton
class BSCTestPancakeSwapFactory(UniswapV2FactoryInterface):
    def __init__(self):
        super().__init__(EthereumNetWorkName.BSCTest, ContractName.PANCAKE_SWAP_FACTORY)


class PancakeSwapPair(UniswapV2PairInterface):
    def __init__(self, name, address):
        super().__init__(EthereumNetWorkName.BSCMain, name, address)


class BSCTestPancakeSwapPair(UniswapV2PairInterface):
    def __init__(self, name, address):
        super().__init__(EthereumNetWorkName.BSCTest, name, address)
