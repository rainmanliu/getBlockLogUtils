# @Time : 8/25/23 4:36 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : main.py
from get_tx_history import EthTransferHistory
import asyncio


async def main():
    e_obj = EthTransferHistory()
    # asyncio.sleep(delay)
    await e_obj.find_all_lock_transactions()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())