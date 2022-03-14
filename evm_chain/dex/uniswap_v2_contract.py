# encoding=utf8
import json
from typing import Optional, Dict, Any, Sequence

from eth_typing import ChecksumAddress
from web3 import Web3
from web3.types import BlockIdentifier

from constant import constant
from constant.ethereum_constant import *
from evm_chain.dex import ethereum
from evm_chain.dex.erc20_contract import ERC20
from evm_chain.dex.my_contract import ContractInterface, MyContract
from util import date_util
from util.singleton import singleton


def str_to_pair_info(pair_info_str) -> (str, int, dict, dict):
    pair_dict = json.loads(pair_info_str)
    return pair_dict.get("address"), pair_dict.get("index"), pair_dict.get("token0"), pair_dict.get("token1")


class RouterFuncName:
    AddLiquidity = "addLiquidity"
    AddLiquidityETH = "addLiquidityETH"
    Factory = "factory"
    GetAmountIn = "getAmountIn"
    GetAmountOut = "getAmountOut"
    GetAmountsIn = "getAmountsIn"
    GetAmountsOut = "getAmountsOut"
    Quote = "quote"
    RemoveLiquidity = "removeLiquidity"
    RemoveLiquidityETH = "removeLiquidityETH"
    RemoveLiquidityETHSupportingFeeOnTransferTokens = "removeLiquidityETHSupportingFeeOnTransferTokens"
    RemoveLiquidityETHWithPermit = "removeLiquidityETHWithPermit"
    RemoveLiquidityETHWithPermitSupportingFeeOnTransferTokens = "removeLiquidityETHWithPermitSupportingFeeOnTransferTokens"
    RemoveLiquidityWithPermit = "removeLiquidityWithPermit"
    SwapETHForExactTokens = "swapETHForExactTokens"
    SwapExactETHForTokens = "swapExactETHForTokens"
    SwapExactETHForTokensSupportingFeeOnTransferTokens = "swapExactETHForTokensSupportingFeeOnTransferTokens"
    SwapExactTokensForETH = "swapExactTokensForETH"
    SwapExactTokensForETHSupportingFeeOnTransferTokens = "swapExactTokensForETHSupportingFeeOnTransferTokens"
    SwapExactTokensForTokens = "swapExactTokensForTokens"
    SwapExactTokensForTokensSupportingFeeOnTransferTokens = "swapExactTokensForTokensSupportingFeeOnTransferTokens"
    SwapTokensForExactETH = "swapTokensForExactETH"
    SwapTokensForExactTokens = "swapTokensForExactTokens"


class UniswapV2RouterInterface(ContractInterface):

    def __init__(self, network, name, address):
        super().__init__(network, name, address, ethereum.get_abi(ContractName.UNISWAP_V2_ROUTER))

    def router_get_amount_out(self, amount_in, reserve_in, reserve_out):
        """
        :param amount_in      付出的token数量
        :param reserve_in     付出的token地址
        :param reserve_out    得到的token地址
        abi:
        {
          "inputs": [
            {
              "internalType": "uint256",
              "name": "amountIn",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "reserveIn",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "reserveOut",
              "type": "uint256"
            }
          ],
          "name": "getAmountOut",
          "outputs": [
            {
              "internalType": "uint256",
              "name": "amountOut",
              "type": "uint256"
            }
          ],
          "stateMutability": "pure",
          "type": "function"
        }
        :return:
        """
        func = self.get_function_by_signature('getAmountOut(uint256,uint256,uint256)')
        return func(amount_in, Web3.toHex(hexstr=ethereum.to_checksum_address(reserve_in)),
                    Web3.toHex(hexstr=ethereum.to_checksum_address(reserve_out))).call()

    def get_amounts_in(self, amount_out, reserve_in, reserve_out):
        """
        :param amount_out     想要得到的reserve_out的金额
        :param reserve_in     付出的token地址
        :param reserve_out    得到的token地址
        abi:
        {"inputs": [{"internalType": "uint256", "name": "amountOut", "type": "uint256"},
                                     {"internalType": "address[]", "name": "path", "type": "address[]"}],
                          "name": "getAmountsIn",
                          "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
                          "stateMutability": "view", "type": "function"}
        :return:
        """
        return self.contract_call(RouterFuncName.GetAmountsIn, amount_out,
                                  [ethereum.to_checksum_address(reserve_out),
                                   ethereum.to_checksum_address(reserve_in)])[0]

    def get_amounts_out(self, amount_in: int, reserve_in: str, reserve_out: str):
        """
        如果支付amount_in个reserve_in会得到多少reserve_out
        :param amount_in      支付的reserve_in的金额， 其中amount_in
        :param reserve_in     付出的token地址
        :param reserve_out    得到的token地址
        abi:
        {"inputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                                      {"internalType": "address[]", "name": "path", "type": "address[]"}],
                           "name": "getAmountsOut",
                           "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
                           "stateMutability": "view", "type": "function"}
        :return:
        """
        return self.contract_call(RouterFuncName.GetAmountsOut, int(amount_in),
                                  [ethereum.to_checksum_address(reserve_in),
                                   ethereum.to_checksum_address(reserve_out)])[1]

    def get_amounts_out_with_token(self, amount_in: float, reserve_in: ERC20, reserve_out: ERC20):
        """
        如果支付amount_in个reserve_in会得到多少reserve_out
        :param amount_in      支付的reserve_in的金额， 其中amount_in
        :param reserve_in     付出的token地址
        :param reserve_out    得到的token地址
        abi:
        {"inputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                                      {"internalType": "address[]", "name": "path", "type": "address[]"}],
                           "name": "getAmountsOut",
                           "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
                           "stateMutability": "view", "type": "function"}
        :return:
        """
        return self.get_amounts_out(amount_in * 10 ** reserve_in.decimals(), reserve_in.get_address(),
                                    reserve_out.get_address())

    def quote(self, amount_a, reserve_a, reserve_b):
        """
        quote
        abi：
        {
          "inputs": [
            {
                  "internalType": "uint256",
                  "name": "amountA",
                  "type": "uint256"
                },
                {
                  "internalType": "uint256",
                  "name": "reserveA",
                  "type": "uint256"
                },
                {
                  "internalType": "uint256",
                  "name": "reserveB",
                  "type": "uint256"
                }
              ],
              "name": "quote",
              "outputs": [
                {
                  "internalType": "uint256",
                  "name": "amountB",
                  "type": "uint256"
                }
              ],
              "stateMutability": "pure",
              "type": "function"
            }
        :return:
        """
        return self.contract_call(RouterFuncName.Quote, amount_a, reserve_a, reserve_b)

    def swap_exact_tokens_for_tokens(self, amount_in, amount_out_min, path, to, wait_seconds):
        """
        代币之间swap
        abi：
        {
          "inputs": [
            {
              "internalType": "uint256",
              "name": "amountIn",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "amountOutMin",
              "type": "uint256"
            },
            {
              "internalType": "address[]",
              "name": "path",
              "type": "address[]"
            },
            {
              "internalType": "address",
              "name": "to",
              "type": "address"
            },
            {
              "internalType": "uint256",
              "name": "deadline",
              "type": "uint256"
            }
          ],
          "name": "swapExactTokensForTokens",
          "outputs": [
            {
              "internalType": "uint256[]",
              "name": "amounts",
              "type": "uint256[]"
            }
          ],
          "stateMutability": "nonpayable",
          "type": "function"
        }
        :return:
        """
        return self.swap_exact_tokens_for_tokens_with_gas(self.gas_price(GasStrategy.FAST), amount_in,
                                                          amount_out_min, path, to, wait_seconds)

    # TODO 在做交易之前应该试算当前的gas费，如果gas费太高不应该交易
    def swap_exact_tokens_for_tokens_with_gas(self, gas_price: int, amount_in, amount_out_min, path, to,
                                              wait_seconds):
        """
        代币之间swap
        """
        deadline = date_util.get_now_timestamp_second() + wait_seconds
        return self.contract_tx_with_gas_price(RouterFuncName.SwapExactTokensForTokens, gas_price, int(amount_in),
                                               int(amount_out_min),
                                               [ethereum.to_checksum_address(address) for address in path],
                                               ethereum.to_checksum_address(to), int(deadline))

    def swap(self, amount_in, amount_out_min, path, wait_seconds):
        """
        代币之间swap,收款人是当前账户
        :return:
        """
        return self.swap_exact_tokens_for_tokens(amount_in, amount_out_min, path, ethereum.default_account.address,
                                                 wait_seconds)

    def swap_use_current_price(self, amount_in, path: [str], slippage_tolerance, wait_seconds):
        """
        以当前价格做代币之间swap，设置滑点
        :param amount_in              支付的金额，此金额的单位是path[0]的最小单位，
        :param path                   兑换路径
        :param slippage_tolerance     滑点
        :param wait_seconds           等待时长
        :return:
        """
        expect = self.get_amounts_out(amount_in, path[0], path[1])
        out_token = ERC20(self.get_network(), constant.BLANK, path[1])
        amount_out_min = (expect * (1 - slippage_tolerance)) * 10 ** out_token.decimals()
        return self.swap_exact_tokens_for_tokens(amount_in, amount_out_min, path, ethereum.default_account.address,
                                                 wait_seconds)

    def swap_use_token(self, slippage_tolerance, wait_seconds, amount_in, path: [ERC20]):
        """
        以当前价格做代币之间swap，设置滑点
        :return:
        """
        amount_in = amount_in * 10 ** path[0].decimals()
        expect = self.get_amounts_out(amount_in, path[0].get_address(), path[1].get_address())
        amount_out_min = expect * (1 - slippage_tolerance)
        return self.swap_exact_tokens_for_tokens(amount_in, amount_out_min,
                                                 [ethereum.to_checksum_address(token.get_address()) for token in path],
                                                 ethereum.default_account.address, wait_seconds)

    def swap_with_gas_price(self, gas, slippage_tolerance, wait_seconds, amount_in, path: [ERC20]):
        """
        以当前价格做代币之间swap，设置滑点
        :return:
        """
        amount_in = amount_in * 10 ** path[0].decimals()
        expect = self.get_amounts_out(amount_in, path[0].get_address(), path[1].get_address())
        amount_out_min = expect * (1 - slippage_tolerance)
        return self.swap_exact_tokens_for_tokens_with_gas(gas, amount_in, amount_out_min,
                                                          [ethereum.to_checksum_address(token.get_address()) for token
                                                           in path],
                                                          ethereum.default_account.address, wait_seconds)


class UniswapV2Router(UniswapV2RouterInterface):
    def __init__(self, network):
        super().__init__(network, ContractName.UNISWAP_V2_ROUTER, "0x7a250d5630b4cf539739df2c5dacb4c659f2488d")


@singleton
class MainNetUniswapV2Router(UniswapV2Router):
    def __init__(self):
        super().__init__(EthereumNetWorkName.Mainnet)


@singleton
class RopstenUniswapV2Router(UniswapV2Router):
    def __init__(self):
        super().__init__(EthereumNetWorkName.Ropsten)


class UniswapV2FactoryInterface(MyContract):
    def __init__(self, network, name):
        super().__init__(network, name)

    def get_pair(self, token_a, token_b):
        """
        获取交易对，abi：
        {
          "constant": true,
          "inputs": [
            {
              "internalType": "address",
              "name": "",
              "type": "address"
            },
            {
              "internalType": "address",
              "name": "",
              "type": "address"
            }
          ],
          "name": "getPair",
          "outputs": [
            {
              "internalType": "address",
              "name": "",
              "type": "address"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :param token_a: token_a的地址
        :param token_b: token_b的地址
        :return: token_a和token_b的交易对的地址，如果没有此交易对则返回0地址
        """
        return self.contract_call("getPair", ethereum.to_checksum_address(token_a),
                                  ethereum.to_checksum_address(token_b))

    def all_pairs(self, index: int):
        """
        获取第index的交易对的地址
        {
          "constant": true,
          "inputs": [
            {
              "internalType": "uint256",
              "name": "",
              "type": "uint256"
            }
          ],
          "name": "allPairs",
          "outputs": [
            {
              "internalType": "address",
              "name": "",
              "type": "address"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :return:
        """
        return self.contract_call("allPairs", index)

    def all_pairs_length(self) -> int:
        """
        获取当前交易对的个数
        {
          "constant": true,
          "inputs": [],
          "name": "allPairsLength",
          "outputs": [
            {
              "internalType": "uint256",
              "name": "",
              "type": "uint256"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :return: 当前交易对的个数
        """
        return self.contract_call("allPairsLength")

    def listen_swap_event(self, argument_filters: Optional[Dict[str, Any]] = None,
                          from_block: Optional[BlockIdentifier] = None, to_block: BlockIdentifier = "latest",
                          address: Optional[ChecksumAddress] = None, topics: Optional[Sequence[Any]] = None,
                          callback=ethereum.print_event):
        self.listen_event_filter("Swap", argument_filters, from_block, to_block, address, topics, callback)


class UniswapV2Factory(UniswapV2FactoryInterface):
    def __init__(self, network):
        super().__init__(network, ContractName.UNISWAP_V2_FACTORY)


@singleton
class MainNetUniswapV2Factory(UniswapV2Factory):
    def __init__(self):
        super().__init__(EthereumNetWorkName.Mainnet)


@singleton
class RopstenUniswapV2Factory(UniswapV2Factory):
    def __init__(self):
        super().__init__(EthereumNetWorkName.Ropsten)


class PairSwapEventKey:
    AMOUNT0_IN = 'amount0In'
    AMOUNT1_IN = 'amount1In'
    AMOUNT0_OUT = 'amount0Out'
    AMOUNT1_OUT = 'amount1Out'
    SENDER = 'sender'
    TO = 'to'


class UniswapV2PairInterface(ContractInterface):

    def __init__(self, network, name, address):
        super().__init__(network, name, address, ethereum.get_abi(ContractName.UNISWAP_V2_PAIR))

    def token0(self):
        """
        获取交易对的第一个token的地址
        abi:
        {
          "constant": true,
          "inputs": [],
          "name": "token0",
          "outputs": [
            {
              "internalType": "address",
              "name": "",
              "type": "address"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :return: 第一个token的地址
        """
        return self.contract_call("token0")

    def token1(self):
        """
        获取交易对的第二个token的地址
        abi: same as token0 method
        :return: 第二个token的地址
        """
        return self.contract_call("token1")

    def price0_cumulative_last(self):
        """
        abi:
        {
          "constant": true,
          "inputs": [],
          "name": "price0CumulativeLast",
          "outputs": [
            {
              "internalType": "uint256",
              "name": "",
              "type": "uint256"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :return:
        """
        return self.contract_call("price0CumulativeLast")

    def price1_cumulative_last(self):
        """
        abi:
        {
          "constant": true,
          "inputs": [],
          "name": "price1CumulativeLast",
          "outputs": [
            {
              "internalType": "uint256",
              "name": "",
              "type": "uint256"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :return:
        """
        return self.contract_call("price1CumulativeLast")

    def get_reserves(self):
        """
        获取储备金
        abi:
        {
          "constant": true,
          "inputs": [],
          "name": "getReserves",
          "outputs": [
            {
              "internalType": "uint112",
              "name": "_reserve0",
              "type": "uint112"
            },
            {
              "internalType": "uint112",
              "name": "_reserve1",
              "type": "uint112"
            },
            {
              "internalType": "uint32",
              "name": "_blockTimestampLast",
              "type": "uint32"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :return: (token0的存储量, token1的存储量, 时间戳（单位秒）)
        """
        return self.contract_call("getReserves")

    def listen_swap_event(self, argument_filters: Optional[Dict[str, Any]] = None,
                          from_block: Optional[BlockIdentifier] = None, to_block: BlockIdentifier = JSONRpc.LATEST,
                          address: Optional[ChecksumAddress] = None, topics: Optional[Sequence[Any]] = None,
                          callback=ethereum.print_event):
        self.listen_event_filter("Swap", argument_filters, from_block, to_block, address, topics, callback)

    def get_swap_event(self, argument_filters: Optional[Dict[str, Any]] = None,
                       from_block: Optional[BlockIdentifier] = None, to_block: BlockIdentifier = JSONRpc.LATEST,
                       address: Optional[ChecksumAddress] = None, topics: Optional[Sequence[Any]] = None):
        return self.get_filter_event("Swap", argument_filters, from_block, to_block, address, topics)


class UniswapV2Pair(UniswapV2PairInterface):
    def __init__(self, network, name, address):
        super().__init__(network, name, address)


class MainNetUniswapV2Pair(UniswapV2Pair):
    def __init__(self, name, address):
        super().__init__(EthereumNetWorkName.Mainnet, name, address)


class RopstenUniswapV2Pair(UniswapV2Pair):
    def __init__(self, name, address):
        super().__init__(EthereumNetWorkName.Ropsten, name, address)
