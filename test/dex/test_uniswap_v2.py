import unittest
from unittest import TestCase

from constant import ethereum_constant
from evm_chain.dex import uniswap_v2, ethereum


class Test(TestCase):
    def test_get_account_balance(self):
        balance, decimals = uniswap_v2.get_account_balance(
            ethereum.get_contract_address(ethereum_constant.EthereumNetWorkName.Mainnet,
                                          ethereum_constant.ContractName.USDT))
        print(f"balance={balance}, decimals={decimals} ")

    def test_uniswap(self):
        usdt_address = ethereum.get_contract_address(ethereum_constant.EthereumNetWorkName.Mainnet,
                                                     ethereum_constant.ContractName.DAI)
        eth_address = ethereum.get_contract_address(ethereum_constant.EthereumNetWorkName.Mainnet,
                                                    ethereum_constant.ContractName.USDT)
        price_input = uniswap_v2.get_price_input(1, eth_address, usdt_address)
        print(price_input)

    def test_get_price_input(self):
        price_input = uniswap_v2.get_price_input(1, "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                                                 "0xca0b3fb6B8dD05c5e489f15164846df061510f78")

        price_input1 = uniswap_v2.get_price_input(1, "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                                                  "0xca0b3fb6B8dD05c5e489f15164846df061510f78")
        print(price_input, price_input1)

    # def test_get_price_output(self):
    #     price_input = uniswap_v2.get_price_output("0x3Ce79A85A65803D463d0EDfB5B83a0A893d05483",
    #                                               "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    #                                               "0xca0b3fb6B8dD05c5e489f15164846df061510f78",
    #                                               1)
    #
    #     price_input1 = uniswap_v2.get_price_output("0x3Ce79A85A65803D463d0EDfB5B83a0A893d05483",
    #                                                "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    #                                                "0xca0b3fb6B8dD05c5e489f15164846df061510f78")
    #     print(price_input, price_input1)

    def test_get_history_price(self):
        prices = uniswap_v2.get_history_price("0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
                                              "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", 10)
        for p in prices:
            print(p)


if __name__ == '__main__':
    unittest.main()
