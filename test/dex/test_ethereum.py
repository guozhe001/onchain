# encoding = utf8
from unittest import TestCase

import eth_utils
from web3 import Web3
from web3.datastructures import AttributeDict

from constant.ethereum_constant import *
from util.exception import CryptoException
from evm_chain.dex import ethereum
from evm_chain.dex import my_contract


def print_attribute_dict(d: AttributeDict):
    ethereum.print_attribute_dict(d)


class Test(TestCase):
    bsc_ethereum = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)

    def test_to_10(self):
        print(Web3.toInt(0xe4e1c0))
        print(Web3.toInt(0x2586efd))
        print(Web3.toInt(0x2586efd) / 35572)
        print(32577350 * 15000000 / 10 ** 18)
        print((eth_utils.to_wei(290.1781, UnitName.GWEI) * 64174))
        # 18771888000000000
        print((eth_utils.to_wei(290.1781, UnitName.GWEI) * 64174) / 15000000)
        print(eth_utils.from_wei(5117431333674330112, UnitName.ETHER))

    def test_contract_call(self):
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
        contract = ethereum_ins.get_contact_by_name(ContractName.BUSD)
        print(type(contract))
        print(contract)
        print(contract.all_functions)
        for func in contract.all_functions():
            print(func)
        result = contract.caller().balanceOf("0xfc18d9812694552737921dF130102579f888888D")
        print(result)

    def test_contract_call1(self):
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.Mainnet)
        contract = ethereum_ins.get_contact("0xde30da39c46104798bb5aa3fe8b9e0e1f348163f", ethereum.get_abi("ERC20"))
        result = ethereum.contract_call(contract, "balanceOf", "0xfc18d9812694552737921dF130102579f888888D")
        print(result)
        self.assertTrue(isinstance(result, int))

    def test_contract_call_bsc(self):
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
        contract = ethereum_ins.get_contact("0x74926b3d118a63f6958922d3dc05eb9c6e6e00c6", ethereum.get_abi("ERC20"))
        result = ethereum.contract_call(contract, "balanceOf", "0xfc18d9812694552737921dF130102579f888888D")
        print(result)
        self.assertTrue(isinstance(result, int))

    def test_contract_call_bsc_exception(self):
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
        contract = ethereum_ins.get_contact("0x74926b3d118a63f6958922d3dc05eb9c6e6e00c6", ethereum.get_abi("ERC20"))
        with self.assertRaises(CryptoException):
            ethereum.contract_call(contract, "balanceOf_test", "0xfc18d9812694552737921dF130102579f888888D")

    def test_get_transaction(self):
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
        transaction = ethereum_ins.get_transaction(
            "0x9af504dc584797a4d5def9fc8eaad85dcfffa799ee9076b6bd1a858026df5c8b")
        print(type(transaction))
        print_attribute_dict(transaction)

    def test_get_transaction_filter_event(self):
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
        transaction_receipt = ethereum_ins.get_transaction_receipt(
            "0x9af504dc584797a4d5def9fc8eaad85dcfffa799ee9076b6bd1a858026df5c8b")
        # print_attribute_dict(transaction_receipt)
        topics = my_contract.MyContract.get_topics(transaction_receipt, "0xe9e7cea3dedca5984780bafc599bd69add087d56")
        print_attribute_dict(topics[0])

    # def test_decode_function_input(self):
    #     ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
    #     transaction = ethereum_ins.get_transaction(
    #         "0x9af504dc584797a4d5def9fc8eaad85dcfffa799ee9076b6bd1a858026df5c8b")
    #     print_attribute_dict(transaction)
    #     func, function_input = ethereum_ins.decode_function_input(transaction)
    #     print(func)
    #     print(function_input)
    #     print(type(function_input))

    def test_get_transaction_receipt(self):
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
        transaction_receipt = ethereum_ins.get_transaction_receipt(
            "0x9af504dc584797a4d5def9fc8eaad85dcfffa799ee9076b6bd1a858026df5c8b")
        print(type(transaction_receipt))
        print_attribute_dict(transaction_receipt)

    def test_gas_price(self):
        for network in [EthereumNetWorkName.Mainnet, EthereumNetWorkName.BSCMain, EthereumNetWorkName.Ropsten,
                        EthereumNetWorkName.FtmMain, EthereumNetWorkName.Rinkeby, EthereumNetWorkName.BSCTest]:
            ethereum_ins = ethereum.get_ethereum(network)
            price = ethereum_ins.gas_price()
            print(f"network={network}, chain_id={ethereum_ins.get_chain_id()},"
                  f" gas_price={price}wei={eth_utils.from_wei(price, UnitName.GWEI)}gwei, height={ethereum_ins.get_height()}")
            self.assertTrue(isinstance(price, int))
            self.assertTrue(price > 0)

    def test_get_block(self):
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.Mainnet)
        block = ethereum_ins.get_block(1120032)
        print(block)
        print_attribute_dict(block)

    def test_get_balance(self):
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
        balance = ethereum_ins.get_balance("0xfc18d9812694552737921dF130102579f888888D")
        print(balance)
        print(eth_utils.from_wei(balance, UnitName.ETHER))
        self.assertTrue(balance > 0)

    def test_contract_tx_exception(self):
        """合约调用测试"""
        ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
        busd = ethereum_ins.get_contact_by_name(ContractName.BUSD)
        with self.assertRaises(CryptoException):
            ethereum_ins.contract_tx(busd, "hello", ethereum.default_account, 10000000)

    def test_add(self):
        # , out_amount=9961028968569408
        print(3.75e+18 / 9961028968569408)

    # tx test start
    # def test_contract_tx_with_gas_price(self):
    #     """合约调用测试"""
    #     ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
    #     print("aaaddd")
    #     busd = ethereum_ins.get_contact_by_name(ContractName.BUSD)
    #     transaction = busd.functions.approve('0xfc18d9812694552737921dF130102579f888888D', 10000).buildTransaction(
    #         {'chainId': ethereum_ins.get_chain_id(), 'from': ethereum.default_account.address,
    #          'nonce': ethereum_ins.w3.eth.getTransactionCount("0x2560be5793F9AA00963e163A1287807Feb897e2F")})
    #     transaction.update({'gas': ethereum_ins.w3.eth.estimate_gas(transaction, block_identifier=None)})
    #     signed_txn = ethereum_ins.w3.eth.account.signTransaction(transaction, ethereum.default_account.privateKey)
    #     txn_hash = ethereum_ins.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    #     receipt = ethereum_ins.wait_for_transaction_receipt(txn_hash)
    #     print_attribute_dict(receipt)
    #
    # def test_contract_tx(self):
    #     """合约调用测试"""
    #     ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
    #     busd = ethereum_ins.get_contact_by_name(ContractName.BUSD)
    #     tx = ethereum_ins.contract_tx(busd, "approve", ethereum.default_account,
    #                                   "0xfc18d9812694552737921dF130102579f888888D", 10000000)
    #     print(tx)
    #     print_attribute_dict(tx)
    #
    # def test_contract_tx_transfer(self):
    #     """合约调用测试"""
    #     ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
    #     busd = ethereum_ins.get_contact("0x55d398326f99059ff775485246999027b3197955",
    #                                     ethereum.get_abi(ContractName.BUSD))
    #     tx = ethereum_ins.contract_tx(busd, "transfer", ethereum.default_account,
    #                                   "0xfc18d9812694552737921dF130102579f888888D", 1)
    #     ethereum.print_attribute_dict(tx)
    #
    # def test_contract_tx_bsc(self):
    #     ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
    #     contract = ethereum_ins.get_contact("0x74926b3d118a63f6958922d3dc05eb9c6e6e00c6", ethereum.get_abi("ERC20"))
    #     tx_hash = contract.functions.approve("0xfc18d9812694552737921dF130102579f888888D", 10000000).transact()
    #     print(tx_hash)
    #     receipt = ethereum_ins.get_transaction_receipt(tx_hash)
    #     ethereum.print_attribute_dict(receipt)
    #
    # def test_transfer(self):
    #     """转账测试"""
    #     ethereum_ins = ethereum.get_ethereum(EthereumNetWorkName.BSCMain)
    #     tx = ethereum_ins.transfer("0xfc18d9812694552737921dF130102579f888888D", 0.001, UnitName.ETHER,
    #                                ethereum.default_account)
    #     ethereum.print_attribute_dict(tx)

    # def test_ftm_contract_tx(self):
    #     ftm_ethereum = ethereum.get_ethereum(EthereumNetWorkName.FtmMain)
    #     rarity = ftm_ethereum.get_contact_by_name(ContractName.RARITY)
    #     transaction = rarity.functions.adventure(2222169).buildTransaction({'from': ethereum.default_account.address,
    #                                                                         'nonce': ftm_ethereum.get_nonce(
    #                                                                             ethereum.default_account.address)})
    #     # tx = ftm_ethereum.contract_tx(rarity, "adventure", ethereum.default_account, 2222169)
    #     tx = ftm_ethereum.sign_and_send(transaction, ethereum.default_account.privateKey)
    #     ethereum.print_attribute_dict(tx)
