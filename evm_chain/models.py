from django.db import models
from django.db.models import Q

from constant import constant
from util.exception import CryptoException


class ERC20TokenColumn:
    ADDRESS = "address"
    NAME = "address"
    SYMBOL = "symbol"
    DECIMALS = "decimals"
    NET_WORK = "net_work"


class PairInfoColumn:
    ADDRESS = "address"
    INDEX = "index"
    TOKEN0 = "token0"
    TOKEN1 = "token1"
    NET_WORK = "net_work"


# 查询方法文档： https://docs.djangoproject.com/en/3.2/topics/db/queries/

class ERC20Token(models.Model):
    # 地址
    address = models.CharField(max_length=256, default=constant.BLANK, verbose_name="地址")
    # 名称
    name = models.CharField(max_length=512, default=None, verbose_name="名称")
    # 符号
    symbol = models.CharField(max_length=128, default=None, verbose_name="符号")
    # 小数位数
    decimals = models.SmallIntegerField(default=0, verbose_name="小数位数")
    # 链名称
    net_work = models.CharField(max_length=32, default=constant.BLANK, verbose_name="链名称")

    def __str__(self):
        return self.address

    @staticmethod
    def get_by_address(net_work, address):
        erc20s = ERC20Token.objects.filter(net_work=net_work, address=address)
        return erc20s[0] if erc20s else None


class PairInfo(models.Model):
    """
    {
      "index": 23107,
      "address": "0xc73de4F1CadCB91B8Eb921ddAaea5cb9baF1dD57",
      "token0": {
        "address": "0x0557Df767419296474C3f551Bb0A0ED4c2DD3380",
        "name": "Universal Gold",
        "symbol": [
          "UPXAU"
        ],
        "decimals": 5
      },
      "token1": {
        "address": "0xF5238462E7235c7B62811567E63Dd17d12C2EAA0",
        "name": "CACHE Gold",
        "symbol": [
          "CGT"
        ],
        "decimals": 8
      }
    }
    """
    # 下标
    index = models.IntegerField(default=None, verbose_name="下标")
    # 地址
    address = models.CharField(max_length=256, default=constant.BLANK, verbose_name="地址")
    # token0地址，不使用id是因为可能token被删除了，但是pair还要记录，如果token被删除则无法记录id
    token0 = models.CharField(max_length=256, default=constant.BLANK, verbose_name="token0地址")
    # token1地址
    token1 = models.CharField(max_length=256, default=constant.BLANK, verbose_name="token1地址")
    # 链名称
    net_work = models.CharField(max_length=32, default=constant.BLANK, verbose_name="链名称")

    def __str__(self):
        return self.address

    @staticmethod
    def get_by_address(net_work, address):
        pairs = PairInfo.objects.filter(net_work=net_work, address=address)
        return pairs[0] if pairs else None

    @staticmethod
    def list_by_token1_address(net_work, token1_address):
        return PairInfo.objects.filter(net_work=net_work, token1=token1_address)

    @staticmethod
    def list_by_token0_address(net_work, token0_address):
        return PairInfo.objects.filter(net_work=net_work, token0=token0_address)

    @staticmethod
    def list_by_token_address(net_work, token_address):
        return PairInfo.objects.filter(Q(net_work=net_work), Q(token1=token_address) | Q(token0=token_address))

    @staticmethod
    def get_by_token_address(net_work, token0_address, token1_address):
        pairs = PairInfo.objects.filter(Q(net_work=net_work), (Q(token1=token0_address) & Q(token0=token1_address)) | (
            Q(token0=token0_address) & Q(token1=token1_address)))
        if not pairs:
            raise CryptoException(
                f"can not find pair from db, where net_work={net_work}, token0_address={token0_address}, "
                f"token1_address={token1_address} ")
        return pairs[0]

    @staticmethod
    def get_by_index(index, net_work):
        return PairInfo.objects.filter(net_work=net_work, index=index)

    @staticmethod
    def get_max_index(network):
        sql = f"""select * from hunter_pairinfo where net_work='{network}' order by `index` desc limit 1"""
        return PairInfo.objects.raw(sql)
