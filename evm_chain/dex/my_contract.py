# encoding=utf8
import logging
import uuid
from enum import Enum
from typing import Optional, Dict, Any, Sequence

from eth_typing.evm import ChecksumAddress
from web3.contract import Contract
from web3.types import BlockIdentifier

from constant.ethereum_constant import GasStrategy
from util.exception import CryptoException
from evm_chain.dex import ethereum

logger = logging.getLogger(__name__)


class MethodType(Enum):
    ContractTx = "contract_tx"
    ContractCall = "contract_call"


class ContractInterface(object):
    def __init__(self, network, name, address, abi):
        print(f"ContractInterface=================network={network}, name={name}, address={address}")
        self.__network = network
        self.__name = name
        self.__address = address
        self.__abi = abi
        self.__ethereum: ethereum.Ethereum = ethereum.get_ethereum(network)
        self.__contract = self.__ethereum.get_contact(address, abi)

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_contract(self) -> Contract:
        return self.__contract

    def get_abi(self) -> list:
        """
        获取当前交易所的abi
        :return:
        """
        return self.__abi

    def get_network(self) -> str:
        return self.__network

    def get_ethereum(self) -> ethereum.Ethereum:
        return self.__ethereum

    def gas_price(self, gas_strategy: GasStrategy = GasStrategy.FAST) -> int:
        return self.__ethereum.gas_price()

    def get_height(self):
        return self.__ethereum.get_height()

    def get_function_by_signature(self, signature):
        """
        根据方法签名获取合约的方法
        @param signature 如identity(uint256,bool)
        """''
        return self.get_contract().get_function_by_signature(signature)

    def contract_call(self, method, *args):
        """
        调用合约，只读
        :param method:  合约方法
        :param args:    合约参数
        :return: TransactionReceiptType
        """
        logger.debug(f"contract call name={self.__name}, address={self.__address}, method={method}, args={args}")
        return ethereum.contract_call(self.__contract, method, *args)

    def contract_tx(self, method, *args):
        """
        写合约
        :param method:  合约方法
        :param args:    合约参数
        :return: TransactionReceiptType
        """
        return self.invoke_contract_with_gas_price(method, self.gas_price(), *args)

    def contract_tx_with_gas_limit(self, method, gas_limit, *args):
        """
        写合约
        :param method:     合约方法
        :param gas_limit:  gas上限
        :param args:       合约参数
        :return: TransactionReceiptType
        """
        return self.get_ethereum().contract_tx_with_gas_limit(self.get_contract(), method, gas_limit,
                                                              ethereum.default_account, *args)

    def contract_tx_with_gas_price(self, method, gas_price: int, *args):
        """
        调用合约
        :param method:        合约方法
        :param gas_price:     gas价格
        :param args:          合约参数
        :return: TransactionReceiptType
        """
        return self.invoke_contract_with_gas_price(method, gas_price, *args)

    def invoke_contract_with_gas_price(self, method, gas_price, *args):
        contract = self.get_contract()
        request_id = str(uuid.uuid4())
        logger.info(
            f"start request_id={request_id}, name={self.get_name()}, address={self.get_address()}, method={method},args={args}")
        result = self.get_ethereum().contract_tx(contract, method, ethereum.default_account, *args)
        logger.info(f"end request_id={request_id},response ={result}")
        return result

    def create_event_filter(self, event_name, argument_filters: Optional[Dict[str, Any]] = None,
                            from_block: Optional[BlockIdentifier] = None,
                            to_block: BlockIdentifier = "latest",
                            address: Optional[ChecksumAddress] = None,
                            topics: Optional[Sequence[Any]] = None):
        if hasattr(self.get_contract().events, event_name):
            event = getattr(self.get_contract().events, event_name)
            return event.createFilter(argument_filters=argument_filters, fromBlock=from_block,
                                      toBlock=to_block, address=address, topics=topics)
        else:
            raise CryptoException(
                f"name={self.get_name()}, address={self.get_address()} have no event:{event_name}")

    def listen_event_filter(self, event_name, argument_filters: Optional[Dict[str, Any]] = None,
                            from_block: Optional[BlockIdentifier] = None, to_block: BlockIdentifier = "latest",
                            address: Optional[ChecksumAddress] = None, topics: Optional[Sequence[Any]] = None,
                            callback=ethereum.print_event):
        event_filter = self.create_event_filter(event_name, argument_filters, from_block, to_block, address, topics)
        ethereum.listen_event_filter(event_filter, callback=callback)

    def get_filter_event(self, event_name, argument_filters: Optional[Dict[str, Any]] = None,
                         from_block: Optional[BlockIdentifier] = None, to_block: BlockIdentifier = "latest",
                         address: Optional[ChecksumAddress] = None, topics: Optional[Sequence[Any]] = None):
        event_filter = self.create_event_filter(event_name, argument_filters, from_block, to_block, address, topics)
        return ethereum.get_filter_event(event_filter)


class MyContract(ContractInterface):
    def __init__(self, network, name):
        super().__init__(network, name, ethereum.get_contract_address(network, name), ethereum.get_abi(name))

    @staticmethod
    def get_topics(tx, target_address):
        return list(
            filter(lambda log: ethereum.to_checksum_address(log.get("address")) == ethereum.to_checksum_address(
                target_address), tx.logs))
