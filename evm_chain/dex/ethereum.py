# encoding=utf8
import json
import logging
import os
import time
from typing import Optional, Dict, Any, Tuple

import hexbytes
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_utils import combomethod
from web3 import Web3
from web3.contract import Contract, ContractFunction
from web3.datastructures import AttributeDict
from web3.types import BlockIdentifier, TxParams

from config import config_util
from constant import constant
from constant.ethereum_constant import EthereumNetWorkName
from util.exception import CryptoException
from util import file_util, date_util


class EthereumProvider:
    INFURA = 'infura'
    ALCHEMY = 'alchemy'
    GETBLOCK = 'getblock'
    MORALIS = 'moralis'


infura_project_id = config_util.get(constant.CONFIG_ETHEREUM_PROJECT_ID, EthereumProvider.INFURA)
alchemy_project_id = config_util.get(constant.CONFIG_ETHEREUM_PROJECT_ID, EthereumProvider.ALCHEMY)
# getblock_project_id = config_util.get(constant.CONFIG_ETHEREUM_PROJECT_ID, EthereumProvider.GETBLOCK)
moralis_project_id = config_util.get(constant.CONFIG_ETHEREUM_PROJECT_ID, EthereumProvider.MORALIS)

os.environ[constant.EnvName.ETHERSCAN_TOKEN] = config_util.get_api_key(constant.EXCHANGE_ETHERSCAN)

logger = logging.getLogger(__name__)


def get_contract_address(network, contract_name):
    """
    根据合约名称获取合约地址
    :param network:        网络名称
    :param contract_name:  合约名称
    :return: 合约地址
    """
    return config_util.get(f"{constant.CONFIG_ADDRESS}.{network}", contract_name)


def get_local_account(private_key) -> LocalAccount:
    """
    根据私钥获取本地账户
    :param private_key: 私钥
    :return:  本地账户
    """
    return Account.from_key(private_key)

default_account = None

try:
    default_account = get_local_account(config_util.get(constant.CONFIG_ETH_ACCOUNT, constant.CONFIG_PRIVATE_KEY))
except Exception as e:
    print("未配置私钥，无法发起交易！")


def get_abi_file(contract_alias):
    """
    获取abi文件的保存路径
    :param contract_alias:   合约名称
    :return:    合约abi的路径
    """
    return config_util.config_path + f"/abi/{contract_alias}.json"


def get_abi(contract_name):
    """
    获取指定合约名称对应的abi
    :param contract_name:  合约名称
    :return: abi
    """
    abi_file = get_abi_file(contract_name)
    if file_util.exists(abi_file):
        abi_str_list = file_util.read_file(abi_file)
        return json.loads(constant.BLANK.join(abi_str_list))
    raise CryptoException(f"contract_name={contract_name} no abi file")


def _filter_contract_events(c: Contract, topic: str,
                            argument_filters: Optional[Dict[str, Any]] = None,
                            from_block: Optional[BlockIdentifier] = None, to_block: BlockIdentifier = "latest",
                            timeout=None):
    if hasattr(c.events, topic):
        event = getattr(c.events, topic)
        event_filter = event.createFilter(argument_filters=argument_filters, fromBlock=from_block, toBlock=to_block)
        start = date_util.get_now_timestamp()
        timeout = 3 if timeout is None else timeout
        # 等待3秒钟
        while date_util.get_now_timestamp() - start < timeout:
            entries = event_filter.get_all_entries()
            if entries:
                return entries
        return []
    raise CryptoException(f"contract={c.address} no event={topic}")


def _get_event_new_entries(event, argument_filters, from_block, to_block):
    event_filter = event.createFilter(argument_filters=argument_filters, fromBlock=from_block, toBlock=to_block)
    return event_filter.get_new_entries()


def contract_call(c: Contract, method, *args):
    """
    read contract
    :param c:
    :param method:
    :param args:
    :return:
    """
    if hasattr(c.caller(), method):
        func = getattr(c.caller(), method)
        return func(*args)
    else:
        raise CryptoException(f"contract={c} have no method={method}")


def contract_func_call(contract_func):
    return contract_func.call()


def to_checksum_address(address):
    """
    官方的检查是否ethsum的地址：
    https://ethsum.netlify.app/
    如果不这么做会报错：
    https://github.com/ethereum/web3.py/issues/740
    :param address:
    :return:
    """
    return Web3.toChecksumAddress(address)


class Ethereum(object):

    def __init__(self, network, endpoint_uri, use_websockets=False):
        self.network = network
        if use_websockets:
            self.w3 = Web3(Web3.WebsocketProvider(endpoint_uri))
        else:
            self.w3 = Web3(Web3.HTTPProvider(endpoint_uri))

    def transfer(self, to_address, amount, unit, from_account: LocalAccount = default_account):
        """
        根据私钥和目的地址转账
        :param from_account: 转出账户
        :param to_address:   转入地址
        :param amount:       转账金额
        :param unit:         转账单位，取值范围：ethereum_constant.UnitName
        :return:  转账结果
        """
        unsigned_tx = {
            'from': from_account.address,
            'nonce': self.get_nonce(from_account.address),
            'to': to_address,
            'value': Web3.toWei(amount, unit),
            'gasPrice': self.gas_price(),
            'chainId': self.get_chain_id(),
        }
        unsigned_tx.update({'gas': self.estimate_gas(unsigned_tx)})
        return self.sign_and_send(unsigned_tx, from_account.privateKey)

    def sign_and_send(self, unsigned_tx: TxParams, private_key):
        signed_txn = self.sign_transaction(unsigned_tx, private_key)
        tx_hash = self.send_raw_transaction(signed_txn)
        return self.wait_for_transaction_receipt(tx_hash)

    def get_transaction(self, tx_hash):
        return self.w3.eth.get_transaction(tx_hash)

    def get_transaction_receipt(self, tx_hash):
        return self.w3.eth.get_transaction_receipt(tx_hash)

    def get_height(self):
        """
        获取当前的区块高度
        :return: 当前的区块高度
        """
        return self.w3.eth.get_block_number()

    def get_balance(self, address):
        return self.w3.eth.get_balance(address)

    @combomethod
    def get_contact(self, address, abi) -> Contract:
        """
        根据合约地址，名称和abi获取合约实例
        :param address:    合约地址
        :param abi:        合约abi
        :return: Contract
        """
        return self.w3.eth.contract(to_checksum_address(str(address)), abi=abi)

    def get_contact_by_name(self, name) -> Contract:
        """
        根据合约地址，名称和abi获取合约实例
        :param name:     合约名称
        :return: Contract
        """
        return self.get_contact(get_contract_address(self.network, name), get_abi(name))

    def gas_price(self):
        return self.w3.eth.gas_price

    def wait_for_transaction_receipt(self, tx_hash):
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_nonce(self, address):
        return self.w3.eth.getTransactionCount(address)

    def estimate_gas(self, transaction):
        return self.w3.eth.estimate_gas(transaction)

    def contract_tx(self, c: Contract, method, from_account: LocalAccount = default_account, *args):
        """
        write contract
        :param from_account: 发起调用的地址
        :param c:      合约实例
        :param method: 合约方法
        :param args: 合约的参数
        :return:
        """
        if hasattr(c.functions, method):
            method_func = getattr(c.functions, method)
            transaction = method_func(*args).buildTransaction({'chainId': self.get_chain_id(),
                                                               'gasPrice': self.gas_price(),
                                                               'from': from_account.address,
                                                               'nonce': self.get_nonce(from_account.address)})
            transaction.update({'gas': self.estimate_gas(transaction)})
            return self.sign_and_send(transaction, from_account.privateKey)
        else:
            raise CryptoException(f"contract={c} have no method={method}")

    def contract_tx_with_gas_limit(self, c: Contract, method, gas_limit=None,
                                   from_account: LocalAccount = default_account, *args):
        """
        write contract
        :param from_account: 发起调用的地址
        :param c:            合约实例
        :param method:       合约方法
        :param gas_limit:    gas上限
        :param args:         合约的参数
        :return:
        """
        if hasattr(c.functions, method):
            method_func = getattr(c.functions, method)
            transaction = method_func(*args).buildTransaction({'chainId': self.get_chain_id(),
                                                               'gasPrice': self.gas_price(),
                                                               'from': from_account.address,
                                                               'nonce': self.get_nonce(from_account.address)})
            transaction.update({'gas': gas_limit if gas_limit else self.estimate_gas(transaction)})
            return self.sign_and_send(transaction, from_account.privateKey)
        else:
            raise CryptoException(f"contract={c} have no method={method}")

    def send_raw_transaction(self, signed_txn):
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    def sign_transaction(self, unsigned_transaction: TxParams, private_key):
        return self.w3.eth.account.signTransaction(unsigned_transaction, private_key)

    def get_block(self, block_identifier: BlockIdentifier):
        return self.w3.eth.get_block(block_identifier)

    def get_chain_id(self):
        return self.w3.eth.chainId

    def decode_function_input(self, tx) -> Tuple['ContractFunction', Dict[str, Any]]:
        return Contract.decode_function_input(tx.input)


class MainNetEthereum(Ethereum):

    def __init__(self):
        super().__init__(EthereumNetWorkName.Mainnet, f"wss://mainnet.infura.io/ws/v3/{infura_project_id}", True)


class BSCMainEthereum(Ethereum):

    def __init__(self):
        super().__init__(EthereumNetWorkName.BSCMain,
                         f"wss://speedy-nodes-nyc.moralis.io/{moralis_project_id}/bsc/mainnet/ws", True)
        # super().__init__(EthereumNetWorkName.BSCMain, f"wss://bsc.getblock.io/mainnet/api_key={getblock_project_id}",
        #                  True)


class RopstenEthereum(Ethereum):

    def __init__(self):
        super().__init__(EthereumNetWorkName.Ropsten, f"wss://ropsten.infura.io/ws/v3/{infura_project_id}", True)


class BSCTestEthereum(Ethereum):

    def __init__(self):
        super().__init__(EthereumNetWorkName.BSCTest,
                         f"wss://speedy-nodes-nyc.moralis.io/{moralis_project_id}/bsc/testnet/ws", True)


class RinkebyEthereum(Ethereum):

    def __init__(self):
        super().__init__(EthereumNetWorkName.Rinkeby, f"wss://rinkeby.infura.io/ws/v3/{infura_project_id}", True)


class FTMEthereum(Ethereum):

    def __init__(self):
        # https://opt-mainnet.g.alchemy.com/v2/{alchemy_project_id}
        super().__init__(EthereumNetWorkName.FtmMain, f"https://opt-mainnet.g.alchemy.com/v2/{alchemy_project_id}")


def get_ethereum(network) -> Ethereum:
    if EthereumNetWorkName.BSCMain == network:
        return BSCMainEthereum()
    if EthereumNetWorkName.Mainnet == network:
        return MainNetEthereum()
    if EthereumNetWorkName.Ropsten == network:
        return RopstenEthereum()
    if EthereumNetWorkName.BSCTest == network:
        return BSCTestEthereum()
    if EthereumNetWorkName.FtmMain == network:
        return FTMEthereum()
    if EthereumNetWorkName.Rinkeby == network:
        return RinkebyEthereum()
    raise CryptoException(f"不支持的网络{network}")


def print_attribute_dict(d: AttributeDict):
    for k, v in d.items():
        if isinstance(v, hexbytes.main.HexBytes):
            logger.info(f"{k}:{type(v)}, {Web3.toHex(v)}")
        else:
            logger.info(f"{k}:{type(v)}, {v}")


def print_event(event):
    if isinstance(event, AttributeDict):
        print_attribute_dict(event)
    elif isinstance(event, hexbytes.main.HexBytes):
        logger.info(Web3.toHex(event))
    logger.info("==========")


def listen_event_filter(event_filter, poll_interval=2, callback=print_event):
    while True:
        for event in event_filter.get_all_entries():
            callback(event)
        time.sleep(poll_interval)


def get_filter_event(event_filter):
    result = []
    for event in event_filter.get_all_entries():
        result.append(event)
    return result
