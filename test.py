# @Time : 8/25/23 4:36 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : test.py
from get_tx_history import NaturalETH, BridgedETH, NaturalNEAR, BridgedNEAR, NaturalErc20, BridgedNep141
import asyncio
from config import Config


def main():
    # erc20合约地址
    # rainbow_eth_address = '0x23Ddd3e3692d1861Ed57EDE224608875809e127f'
    # test_from_block = 17967800
    # test_from_block =
    MarcoAddress = '0x4fE898667Ba84f2691b4dBf1bfD98Ff7BBAAcbEE'
    print("***** eth lock txs")
    NaturalETH().find_all_transactions(sender=MarcoAddress)
    print("***** eth burn txs")
    BridgedETH().find_all_transactions(sender='sunhao.near')

    print("***** near lock txs")
    NaturalNEAR().find_all_transactions(sender='sunhao.near')
    print("***** near burn txs")
    BridgedNEAR().find_all_transactions(sender=MarcoAddress)

    erc20_lock_list, erc20_burn_list = [], []
    for token in Config.FEATURED_ERC20.value:
        lock_list = NaturalErc20().find_all_transactions(sender=MarcoAddress, erc20_address=token)
        erc20_lock_list.extend(lock_list)
        burn_list = BridgedNep141().find_all_transactions(sender=MarcoAddress, erc20_address=token)
        erc20_burn_list.extend(burn_list)

    print(f"***** Erc20: lock txs")
    print(erc20_lock_list)
    print(f"***** BridgeErc20:burn txs")
    print(erc20_burn_list)

if __name__ == '__main__':
    main()