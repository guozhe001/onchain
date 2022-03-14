import json
import logging
import unittest
from unittest import TestCase

import eth_utils

from constant.ethereum_constant import EthereumNetWorkName, ContractName
from evm_chain.dex import ethereum, erc20_contract
from evm_chain.dex.erc20_contract import ERC20Constant, ERC20

test_network = EthereumNetWorkName.Rinkeby


class TestERC20(TestCase):

    def test_print_erc20_abi(self):
        abi = ethereum.get_abi(ERC20Constant.ERC20)
        for a in abi:
            # if a.get("type") != "function":
            # func_name = a.get('name')
            # if func_name:
            #     print(f"METHOD_{func_name.upper()} = \"{func_name}\"")
            if a.get("type") == "event":
                print(f"name={a.get('name')}: {json.dumps(a)}")

    def test_decimals(self):
        dai = ERC20(EthereumNetWorkName.Rinkeby, ContractName.DAI,
                    ethereum.get_contract_address(test_network, ContractName.DAI))
        decimals = dai.decimals()
        name = dai.name()
        symbol = dai.symbol()
        total_supply = dai.total_supply()
        print(decimals)
        print(name)
        print(total_supply)
        self.assertEqual(18, decimals)
        self.assertEqual("Dai", name)
        self.assertEqual("DAI", symbol)
        balance = dai.balance_of(ethereum.default_account.address)
        print(balance)
        b = dai.balance_of_default_account()
        self.assertEqual(balance, b)

    def test_balanceOf(self):
        usdt = ERC20(EthereumNetWorkName.BSCMain, "usdt", "0x55d398326f99059fF775485246999027B3197955")
        balance_wei = usdt.balance_of("0x2560be5793F9AA00963e163A1287807Feb897e2F")
        # 5117431333674330112
        # 5117431333674329350
        logging.info(
            f"balance_wei={balance_wei}, balance_ether={eth_utils.from_wei(balance_wei, erc20_contract.UnitName.ETHER)}")

    # tx start
    # def test_approve_max(self):
    #     dai = ERC20(test_network, ContractName.DAI, ethereum.get_contract_address(test_network, ContractName.DAI))
    #     approve_max = dai.approve_max(ethereum.get_contract_address(EthereumNetWorkName.Mainnet,
    #                                                                 ContractName.UNISWAP_V2_ROUTER))
    #     test_ethereum.print_attribute_dict(approve_max)
    #
    # def test_transfer_from(self):
    #     dai = ERC20(EthereumNetWorkName.BSCMain, "USDT", "0x8076c74c5e3f5852037f32ff0093eeb8c8add8d3")
    #     tx = dai.transfer_from("0xfc18d9812694552737921dF130102579f888888D",
    #                            "0x2560be5793F9AA00963e163A1287807Feb897e2F", 1, UnitName.WEI)
    #     print(tx)
    #     test_ethereum.print_attribute_dict(tx)
    #
    # def test_transfer(self):
    #     dai = ERC20(EthereumNetWorkName.BSCMain, "DOGGY", "0x44bEb847Cc2a9d1166868Bd139A919cc3329Fb96")
    #     transfer = dai.transfer("0xfc18d9812694552737921dF130102579f888888D", 1, UnitName.GWEI)
    #     test_ethereum.print_attribute_dict(transfer)
    #
    # def test_approve1(self):
    #     dai = ERC20(EthereumNetWorkName.BSCMain, "DOGGY", "0x44bEb847Cc2a9d1166868Bd139A919cc3329Fb96")
    #     tx = dai.approve("0xfc18d9812694552737921dF130102579f888888D", 1, UnitName.ETHER)
    #     print(tx)
    #     test_ethereum.print_attribute_dict(tx)
    #
    # def test_allowance(self):
    #     dai = ERC20(EthereumNetWorkName.BSCMain, "USDT", "0x8076c74c5e3f5852037f32ff0093eeb8c8add8d3")
    #     allowance = dai.allowance("0xfc18d9812694552737921dF130102579f888888D", ethereum.default_account.address)
    #     print(allowance)


if __name__ == '__main__':
    unittest.main()
