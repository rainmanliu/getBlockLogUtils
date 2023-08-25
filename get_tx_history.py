# @Time : 8/25/23 4:37 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : get_tx_history.py.py
from typing import List
import ctc

import web3


class EthTransferHistory():

    async def find_all_lock_transactions(self):
        events = await ctc.async_get_events(
            contract_address='0x23Ddd3e3692d1861Ed57EDE224608875809e127f',
            event_name='Lock',
            start_block=17967800
        )

        print(events)

    def find_all_burn_transactions(self):
        pass


class NearTransferHistory():

    def find_all_lock_transactions(self):
        pass

    def find_all_withdraw_transactions(self):
        pass


class TokensTransferHistory():
    """
    nep141 - erc20
    """
    # Default Erc20 token
    TOKENS = []

    def __init__(self, tokens: List[str]):
        self.tokens = tokens

    def find_erc20_lock_transactions(self):
        pass

    def find_nep141_burn_transactions(self, fromBlock: str, toBlock: str, sender: str, erc20Address: str):
        """
        Find all withdraw(burn) transactions sending nep141Address tokens from NEAR to Ethereum.
        :param fromBlock:
        :param toBlock:
        :param sender:
        :param erc20Address:
        :return:
        """
        pass
