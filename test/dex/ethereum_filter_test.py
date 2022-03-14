from constant.ethereum_constant import ContractName, EthereumNetWorkName
from evm_chain.dex import erc20_contract
from evm_chain.dex import ethereum
from evm_chain.dex import pancake_swap
from evm_chain.dex.erc20_contract import ERC20
from evm_chain.dex.pancake_swap_contract import PancakeSwapRouter, PancakeSwapFactory, PancakeSwapPair
from evm_chain.dex.uniswap_v2_contract import PairSwapEventKey

bscmain = EthereumNetWorkName.BSCMain

xwg = ERC20(bscmain, "xwg", "0x6b23c89196deb721e6fd9726e6c76e4810a464bc")
usdt = ERC20(bscmain, "usdt", "0x55d398326f99059ff775485246999027b3197955")
router = PancakeSwapRouter(bscmain)
factory = PancakeSwapFactory()


def print_event(event):
    args = event.get("args")
    # 这里能够验证，当pair被router调用时，不会出现同一个币既有in又有out的情况；这些都是正常兑换
    if args.get(PairSwapEventKey.AMOUNT0_IN) and args.get(PairSwapEventKey.AMOUNT0_OUT):
        print(event)
    if args.get(PairSwapEventKey.AMOUNT1_IN) and args.get(PairSwapEventKey.AMOUNT1_OUT):
        print(event)
    ethereum.print_event(event)


def pair_events():
    token0 = ContractName.BUSD
    token1 = ContractName.WBNB
    pair_address = factory.get_pair(ethereum.get_contract_address(bscmain, token0),
                                    ethereum.get_contract_address(bscmain, token1))
    name = f"pair_{token0}_{token1}={pair_address}"
    pair = PancakeSwapPair(name, pair_address)
    print(name)
    argument_filters = {PairSwapEventKey.SENDER: router.get_address()}
    pair.listen_swap_event(argument_filters, from_block=factory.get_height(), callback=print_event)


def contract_event():
    event_filter = usdt.get_contract().events.Transfer.createFilter(fromBlock='latest')
    ethereum.listen_event_filter(event_filter, callback=print_event)


def event_from_my_contract():
    usdt.listen_approval_event(argument_filters=erc20_contract.get_event_approve_argument_filters(
        owner="0x2560be5793F9AA00963e163A1287807Feb897e2F"), from_block=11297906, callback=print_event)


def busd_approve_event():
    busd = ERC20(bscmain, "busd", "0xe9e7cea3dedca5984780bafc599bd69add087d56")
    busd.listen_approval_event(argument_filters=erc20_contract.get_event_approve_argument_filters(
        owner="0x2560be5793F9AA00963e163A1287807Feb897e2F", spender=router.get_address()), from_block=11297906,
        callback=print_event)


def new_event():
    event_filter = usdt.get_ethereum().w3.eth.filter('latest')
    ethereum.listen_event_filter(event_filter)


def get_history_price():
    bnb = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
    usdt = "0x55d398326f99059ff775485246999027b3197955"
    pair_address = PancakeSwapFactory().get_pair(bnb, usdt)
    print(pair_address)
    price = pancake_swap.get_history_price(pair_address, PancakeSwapPair("xwg_usdt", pair_address).token0(), bnb, 5)
    print(f"len={len(price)}")
    for p in price:
        print(p)


if __name__ == "__main__":
    get_history_price()
