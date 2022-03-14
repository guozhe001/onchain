import json
from unittest import TestCase

from constant.ethereum_constant import *
from evm_chain.dex import erc20_contract, uniswap_v2_contract, ethereum
from evm_chain.dex.uniswap_v2_contract import UniswapV2Pair, UniswapV2Factory, \
    UniswapV2Router

network = EthereumNetWorkName.Mainnet
router = UniswapV2Router(network)
dai = erc20_contract.ERC20(network, ContractName.DAI, ethereum.get_contract_address(network, ContractName.DAI))
uni = erc20_contract.ERC20(network, ContractName.UNI, ethereum.get_contract_address(network, ContractName.UNI))
usdt = erc20_contract.ERC20(network, ContractName.USDT, ethereum.get_contract_address(network, ContractName.USDT))
factory = UniswapV2Factory(network)
test_pair = UniswapV2Pair(network, "index1", factory.all_pairs(1))


def print_abi(abi):
    for a in abi:
        # if a.get("type") != "function":
        print(f"name={a.get('name')}: {json.dumps(a)}\n")
        # print(json.dumps(a))
        # for k, v in a.items():
        #     print(k, v)


def print_events(entries):
    for e in entries:
        print(e)


class Test(TestCase):
    def test_get_abi(self):
        print_abi(router.get_abi())

    # def test_router_get_amount_out(self):
    # 这个没有测试通过，因为方法签名和我的入参不一致导致，还没有找到解决方法
    #     out = router.router_get_amount_out(eth_utils.currency.to_wei(0.1, UnitName.ETHER),
    #                                        ethereum.get_contract_address(network, ContractName.WETH9),
    #                                        ethereum.get_contract_address(network, ContractName.UNI))
    #     self.assertTrue(out > 0)
    #     # uni_decimals = uni.decimals()
    #     balance = dai.balance_of(ethereum.default_account)
    #     print(balance)

    # def test_quote(self):
    #     result = router.quote(dai.balance_of_default_account(), dai.get_address(),
    #                           ethereum_util.get_contract_address(ContractName.WETH9))
    #     print(result)

    def test_balance_of_default_account(self):
        print(usdt.balance_of_default_account())
        print(type(usdt.balance_of_default_account()))

    #
    # def test_swap_exact_tokens_for_tokens(self):
    #     tokens = router.swap_exact_tokens_for_tokens(eth_utils.currency.to_wei(1, UnitName.GWEI),
    #                                                  eth_utils.currency.to_wei(0, UnitName.ETHER),
    #                                                  [dai.get_address(), usdt.get_address()],
    #                                                  ethereum_util.get_default_account(),
    #                                                  date_util.get_now_timestamp_second() + 10)
    #     print(tokens)

    def test_print_factory_abi(self):
        print_abi(factory.get_abi())

    def test_get_pair(self):
        pair_address = factory.get_pair(uni.get_address(), dai.get_address())
        pair_name = f"{uni.get_name()}_{dai.get_name()}"
        uni_dai = UniswapV2Pair(network, pair_name, pair_address)
        print(f"pair_name={pair_name}, pair_address={pair_address}")
        print_abi(uni_dai.get_abi())

    def test_pair_token(self):
        pair_address = factory.get_pair(uni.get_address(), dai.get_address())
        uni_dai = UniswapV2Pair(network, "UNI_DAI", pair_address)
        token_0 = uni_dai.token0()
        token_1 = uni_dai.token1()
        self.assertEqual(ethereum.to_checksum_address(token_0), ethereum.to_checksum_address(uni.get_address()))
        self.assertEqual(token_1, ethereum.to_checksum_address(dai.get_address()))

    def test_all_pairs(self):
        index = 100
        pair_address = factory.all_pairs(index)
        print(f"the index ={index}'s pair's address is :{pair_address}")

    # def test_get_pair_and_save(self):
    #     start_index = 5010
    #     for i in range(1):
    #         end_index = start_index + 5
    #         print(f"start_index={start_index}, end_index={end_index}===================\n")
    #         uniswap_v2_contract.get_pairs_and_save(start_index, end_index)
    #         start_index = end_index

    def test_all_pairs_length(self):
        print(factory.all_pairs_length())

    def test_get_reserves(self):
        _reserve0, _reserve1, _blockTimestampLast = test_pair.get_reserves()
        print(f"_reserve0={_reserve0}, _reserve1={_reserve0}, _blockTimestampLast={_blockTimestampLast}")

    # def test_pair_events(self):
    #     token0 = ContractName.UNI
    #     token1 = ContractName.WETH9
    #     pair_address = factory.get_pair(ethereum.get_contract_address(network, token0),
    #                                     ethereum.get_contract_address(network, token1))
    #     name = f"pair_{token0}_{token1}={pair_address}"
    #     print(name)
    #     uniswap_v_pair = MainNetUniswapV2Pair(name, pair_address)
    #     argument_filters = {PairSwapEventKey.SENDER: router.get_address()}
    #     to_block = ethereum.get_ethereum(network).get_height()
    #     from_block = to_block - 1000
    #     entries = uniswap_v_pair.listen_swap_event(argument_filters, from_block, to_block)
    #     if entries:
    #         # entries是按照区块高度的正序排序
    #         for e in entries:
    #             args = e.get("args")
    #             # 这里能够验证，当pair被router调用时，不会出现同一个币既有in又有out的情况；这些都是正常兑换
    #             if args.get(PairSwapEventKey.AMOUNT0_IN) and args.get(
    #                 PairSwapEventKey.AMOUNT0_OUT):
    #                 print(e)
    #             if args.get(PairSwapEventKey.AMOUNT1_IN) and args.get(
    #                 PairSwapEventKey.AMOUNT1_OUT):
    #                 print(e)
    #             print(e)

    # def test_listen_address_events(self):
    #     token0 = ContractName.USDT
    #     token1 = ContractName.WETH9
    #     pair_address = factory.get_pair(ethereum.get_contract_address(network, token0),
    #                                     ethereum.get_contract_address(network, token1))
    #     # argument_filters = {PairSwapEventKey.SENDER.value: router.get_address()}
    #     ethereum_ins = ethereum.get_ethereum(network)
    #     ethereum_ins.listen_address_events(print_events, address=pair_address, from_block=ethereum_ins.get_height(),
    #                                        abi=ethereum.get_abi(ContractName.UNISWAP_V2_PAIR), topic="Swap")

    def test_str_to_pair_info(self):
        pair_str = """{"index": 0, "address": "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc", "token0": {"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "name": "USD Coin", "symbol": "USDC", "decimals": 6}, "token1": {"address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "name": "Wrapped Ether", "symbol": "WETH", "decimals": 6}}"""
        result = uniswap_v2_contract.str_to_pair_info(pair_str)
        for r in result:
            print(r)
            print(type(r))
