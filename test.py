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
    # NaturalETH().find_all_transactions(sender=MarcoAddress)
    # BridgedETH().find_all_transactions(sender='enoshka13.near', from_block='1643483291725895435', to_block='1643483902107328855', receive_account="app.nearcrowd.near")
    # NaturalNEAR().find_all_transactions(sender='enoshka13.near', from_block='1643483291725895435', to_block='1643483902107328855', receive_account="app.nearcrowd.near")
    # BridgedNEAR().find_all_transactions(sender=MarcoAddress)
    for token in Config.FEATURED_ERC20.value:
        # NaturalErc20().find_all_transactions(sender=MarcoAddress, erc20_address=token)
        BridgedNep141().find_all_transactions(sender=MarcoAddress, erc20_address=token)


if __name__ == '__main__':
    main()