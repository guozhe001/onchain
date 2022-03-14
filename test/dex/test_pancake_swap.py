from unittest import TestCase

from evm_chain.dex import pancake_swap
from evm_chain.dex.pancake_swap import *

bscmain = EthereumNetWorkName.BSCMain


class Test(TestCase):
    def test_get_account_balance(self):
        balance = pancake_swap.get_account_balance(ethereum.get_contract_address(bscmain, ContractName.BUSD))
        print(balance)

    def test_get_address_balance(self):
        balance, decimals = pancake_swap.get_address_balance(ethereum.get_contract_address(bscmain, ContractName.FOXY),
                                                             "0xfc18d9812694552737921dF130102579f888888D")
        print(balance / 10 ** decimals)

    def test_list(self):
        nums = [1, 2, 3]
        print(nums[:10])

    def test_allowance(self):
        a = pancake_swap.allowance("0x55d398326f99059ff775485246999027b3197955")
        print(a)
        print(type(a))

    def test_get_price_out(self):
        out = pancake_swap.get_price_out(1, ethereum.get_contract_address(bscmain, ContractName.WBNB),
                                         ethereum.get_contract_address(bscmain, ContractName.USDT))
        print(out)
        # print(eth_utils.from_wei(out))
