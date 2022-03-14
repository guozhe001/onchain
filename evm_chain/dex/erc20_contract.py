# encoding=utf8
from typing import Optional, Dict, Any, Sequence

import eth_utils
from eth_typing import ChecksumAddress
from web3.types import BlockIdentifier

from constant.ethereum_constant import UnitName
from evm_chain.dex import ethereum
from evm_chain.dex.my_contract import ContractInterface
from util.exception import CryptoException


def get_event_transfer_argument_filters(_from=None, to=None, value=None):
    if _from or to or value:
        result = {}
        if _from:
            result.update({"from": _from})
        if to:
            result.update({"to": to})
        if value:
            result.update({"value": value})
        return result
    else:
        raise CryptoException("不能所有参数都为None")


def get_event_approve_argument_filters(owner=None, spender=None, value=None):
    if owner or spender or value:
        result = {}
        if owner:
            result.update({"owner": owner})
        if spender:
            result.update({"spender": spender})
        if value:
            result.update({"value": value})
        return result
    else:
        raise CryptoException("不能所有参数都为None")


class ERC20Constant:
    ERC20 = "ERC20"
    # ERC20中的方法名称
    METHOD_NAME = "name"
    METHOD_APPROVE = "approve"
    METHOD_TOTAL_SUPPLY = "totalSupply"
    METHOD_TRANSFER_FROM = "transferFrom"
    METHOD_DECIMALS = "decimals"
    METHOD_BALANCE_OF = "balanceOf"
    METHOD_SYMBOL = "symbol"
    METHOD_TRANSFER = "transfer"
    METHOD_ALLOWANCE = "allowance"


class ERC20(ContractInterface):
    def __init__(self, network, name, address):
        super().__init__(network, name, address, ethereum.get_abi(ERC20Constant.ERC20))

    def approve(self, spender, amount, unit):
        """
        授权某个erc20给spender,abi:
        {
          "constant": false,
          "inputs": [
            {
              "name": "_spender",
              "type": "address"
            },
            {
              "name": "_value",
              "type": "uint256"
            }
          ],
          "name": "approve",
          "outputs": [
            {
              "name": "",
              "type": "bool"
            }
          ],
          "payable": false,
          "stateMutability": "nonpayable",
          "type": "function"
        }
        :param spender:         需要授权的地址
        :param amount:          需要授权的金额
        :param unit:            金额的单位
        :return:
        """
        return self.contract_tx(ERC20Constant.METHOD_APPROVE, ethereum.to_checksum_address(spender),
                                eth_utils.to_wei(amount, unit))

    def approve_max(self, spender):
        """
        授权某个erc20给spender
        :param spender:         需要授权的地址
        :return:
        """
        return self.approve(spender, self.total_supply(), UnitName.WEI)

    def total_supply(self):
        """
        获取erc20的total_supply,abi:
                {
          "constant": true,
          "inputs": [],
          "name": "totalSupply",
          "outputs": [
            {
              "name": "",
              "type": "uint256"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :return: 指定erc20 token的总供应量
        """
        return self.contract_call(ERC20Constant.METHOD_TOTAL_SUPPLY)

    def name(self):
        """
        获取名称,abi:
        {
          "constant": true,
          "inputs": [],
          "name": "name",
          "outputs": [
            {
              "name": "",
              "type": "string"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :return:  名称
        """
        return self.contract_call(ERC20Constant.METHOD_NAME)

    def transfer_from(self, _from, to, value, unit):
        """
        转账，abi
        {
          "constant": false,
          "inputs": [
            {
              "name": "_from",
              "type": "address"
            },
            {
              "name": "_to",
              "type": "address"
            },
            {
              "name": "_value",
              "type": "uint256"
            }
          ],
          "name": "transferFrom",
          "outputs": [
            {
              "name": "",
              "type": "bool"
            }
          ],
          "payable": false,
          "stateMutability": "nonpayable",
          "type": "function"
        }
        :return:  名称
        """
        return self.contract_tx(ERC20Constant.METHOD_TRANSFER_FROM, ethereum.to_checksum_address(_from),
                                ethereum.to_checksum_address(to), eth_utils.to_wei(value, unit))

    def transfer(self, to, value, unit):
        """
        转账，abi
        {"constant": false, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
         "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "payable": false,
         "stateMutability": "nonpayable", "type": "function"}
        :return: 交易信息
        """
        return self.contract_tx(ERC20Constant.METHOD_TRANSFER, to, eth_utils.to_wei(value, unit))

    def decimals(self):
        """
        abi:
        {
          "constant": true,
          "inputs": [],
          "name": "decimals",
          "outputs": [
            {
              "name": "",
              "type": "uint8"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        :return:
        """
        return self.contract_call(ERC20Constant.METHOD_DECIMALS)

    def balance_of(self, address):
        """
        获取余额，即指定地址有多少当前的token
        @:param address 需要获取余额的地址
        abi:
        {
          "constant": true,
          "inputs": [
            {
              "name": "_owner",
              "type": "address"
            }
          ],
          "name": "balanceOf",
          "outputs": [
            {
              "name": "balance",
              "type": "uint256"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        """
        return self.contract_call(ERC20Constant.METHOD_BALANCE_OF, address)

    def balance_of_default_account(self):
        """
        获取余额，即指定地址有多少当前的token
        @:param address 需要获取余额的地址
        abi:
        {
          "constant": true,
          "inputs": [
            {
              "name": "_owner",
              "type": "address"
            }
          ],
          "name": "balanceOf",
          "outputs": [
            {
              "name": "balance",
              "type": "uint256"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        """
        return self.balance_of(ethereum.default_account.address)

    def symbol(self):
        """
        获取余额，即指定地址有多少当前的token
        @:param address 需要获取余额的地址
        abi:
        {
          "constant": true,
          "inputs": [],
          "name": "symbol",
          "outputs": [
            {
              "name": "",
              "type": "string"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
        """
        return self.contract_call("symbol")

    def allowance(self, _owner, _spender):
        """
        获取余额，即指定地址有多少当前的token
        @:param address 需要获取余额的地址
        abi:
        {"constant": true,
        "inputs": [{"name": "_owner", "type": "address"},{"name": "_spender", "type": "address"}],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": false, "stateMutability": "view", "type": "function"}
        """
        return self.contract_call("allowance", _owner, _spender)

    def listen_approval_event(self, argument_filters: Optional[Dict[str, Any]] = None,
                              from_block: Optional[BlockIdentifier] = None, to_block: BlockIdentifier = "latest",
                              address: Optional[ChecksumAddress] = None, topics: Optional[Sequence[Any]] = None,
                              callback=ethereum.print_event):
        """
        abi:
        {"anonymous": false, "inputs": [{"indexed": true, "name": "owner", "type": "address"},
                                        {"indexed": true, "name": "spender", "type": "address"},
                                        {"indexed": false, "name": "value", "type": "uint256"}], "name": "Approval",
         "type": "event"}
        """
        self.listen_event_filter("Approval", argument_filters, from_block, to_block, address, topics, callback)

    def listen_transfer_filter(self, argument_filters: Optional[Dict[str, Any]] = None,
                               from_block: Optional[BlockIdentifier] = None, to_block: BlockIdentifier = "latest",
                               address: Optional[ChecksumAddress] = None, topics: Optional[Sequence[Any]] = None,
                               callback=ethereum.print_event):
        """
        abi:
        {"anonymous": false, "inputs": [{"indexed": true, "name": "from", "type": "address"},
                                        {"indexed": true, "name": "to", "type": "address"},
                                        {"indexed": false, "name": "value", "type": "uint256"}], "name": "Transfer",
         "type": "event"}
         """
        self.listen_event_filter("Transfer", argument_filters, from_block, to_block, address, topics, callback)
