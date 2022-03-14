from unittest import TestCase

from constant.ethereum_constant import GasStrategy


class TestGasStrategy(TestCase):
    def test_enum_name(self):
        for gas_strategy in GasStrategy:
            print(f"{gas_strategy}={gas_strategy.name},{gas_strategy.value}")
