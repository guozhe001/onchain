from unittest import TestCase

import web3.eth

from evm_chain.dex.erc20_contract import ERC20
from evm_chain.dex.pancake_swap_contract import *
from util import str_util

bscmain = EthereumNetWorkName.BSCMain

busd_address = ethereum.get_contract_address(bscmain, ContractName.BUSD)
wbnb_address = ethereum.get_contract_address(bscmain, ContractName.WBNB)
xwg = ERC20(bscmain, "xwg", "0x6b23c89196deb721e6fd9726e6c76e4810a464bc")
usdt = ERC20(bscmain, "usdt", "0x55d398326f99059ff775485246999027b3197955")
router = PancakeSwapRouter(bscmain)
factory = PancakeSwapFactory()


def print_abi(abi):
    for a in abi:
        if a.get("type") == "function":
            # print(f"name={a.get('name')}: {json.dumps(a)}")
            # print(f"""{str_util.capitalize(a.get('name'))} = \"{a.get('name')\"}""")
            print('{} = "{}"'.format(str_util.capitalize(a.get('name')), a.get('name')))


class Test(TestCase):

    def test_print_router_abi(self):
        print_abi(router.get_abi())
        print(router)

    def test_pair_abi(self):
        pair_address = PancakeSwapFactory().get_pair(wbnb_address, busd_address)
        self.assertEqual("0x58F876857a02D6762E0101bb5C46A8c1ED44Dc16", pair_address)
        bnb_busd = PancakeSwapPair("BNB-BUSD", pair_address)
        print_abi(bnb_busd.get_abi())
        print(pair_address)

    def test_get_amounts_in(self):
        out = router.get_amounts_in(1, wbnb_address, busd_address)
        print(out)
        self.assertTrue(out > 1)

    def test_get_amounts_out(self):
        out = router.get_amounts_out(1, wbnb_address, busd_address)
        print(out)
        self.assertTrue(out > 1)

    def test_get_amounts_out1(self):
        out = router.get_amounts_out(0.1 * 10 ** usdt.decimals(), usdt.get_address(), xwg.get_address())
        print(f"use {0.1} usdt can swap {out / 10 ** xwg.decimals()} {xwg.get_name()}")
        self.assertTrue(out > 0)

    def test_get_amounts_out2(self):
        money = 6.737174427205205
        out = router.get_amounts_out(money * 10 ** usdt.decimals(), usdt.get_address(), xwg.get_address())
        print(out / 10 ** xwg.decimals())
        print(f"use {money} {usdt.get_name()} can swap {out / 10 ** xwg.decimals()} {xwg.get_name()}")
        self.assertTrue(out > 0)

    def test_hex(self):
        print(eth_utils.decode_hex("f3d29cd97c6b20"))
        print(web3.Web3.toInt(hexstr="0x00000000000000000000000000000000000000000000000000f3d29cd97c6b20"))

    # tx test start
    # def test_swap_use_token(self):
    #     balance = xwg.balance_of_default_account()
    #     print(balance)
    #     decimals_ = eth_utils.to_wei(0.1 * 10 ** xwg.decimals(), UnitName.WEI)
    #     print(decimals_)
    #     swap_tx = router.swap(decimals_, 0.009 * 10 ** usdt.decimals(), [usdt.get_address(), xwg.get_address()], 20)
    #     ethereum.print_attribute_dict(swap_tx)
    #     xwg_events = MyContract.get_topics(swap_tx, xwg.get_address())
    #     for event in xwg_events:
    #         ethereum.print_attribute_dict(event)

    # def test_swap_exact_tokens_for_tokens_with_gas(self):
    #     xwg_contract = ERC20(bscmain, "xwg", xwg)
    #     usdt_contract = ERC20(bscmain, "usdt", usdt)
    #     balance = usdt_contract.balance_of_default_account()
    #     print(balance)
    #     tx = router.swap_use_token(0.01, 20, 0.1, [usdt_contract, xwg_contract])
    #     ethereum.print_attribute_dict(tx)
