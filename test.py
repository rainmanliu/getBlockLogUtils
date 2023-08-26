# @Time : 8/25/23 4:36 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : test.py
from get_tx_history import NaturalETH, BridgedETH, NaturalNEAR, BridgedNEAR, NaturalErc20, BridgedNep141
import asyncio
from config import Config
import asyncio
from aiohttp import ClientSession
import time


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
    #
    print("***** near lock txs")
    NaturalNEAR().find_all_transactions(sender='sunhao.near')
    print("***** near burn txs")
    BridgedNEAR().find_all_transactions(sender=MarcoAddress)

    erc20_lock_list, erc20_burn_list = [], []

    MarcoErc20Address = 'sunhao.near'
    for token in Config.FEATURED_ERC20.value:
        lock_list = NaturalErc20().find_all_transactions(sender=MarcoAddress, erc20_address=token)
        erc20_lock_list.extend(lock_list)
        # burn_list = BridgedNep141().find_all_transactions(sender=MarcoErc20Address, erc20_address=token)
        # erc20_burn_list.extend(burn_list)

    print(f"***** Erc20: lock txs")
    print(erc20_lock_list)
    # print(f"***** BridgeErc20:burn txs")
    # print(erc20_burn_list)


async def get_async_bridge_erc20():
    MarcoErc20Address = 'sunhao.near'
    task_list = []
    for token in Config.FEATURED_ERC20.value:
        task = asyncio.create_task(
            BridgedNep141().async_find_all_transactions(
                sender=MarcoErc20Address, erc20_address=token
            )
        )
        task_list.append(task)
    done, pending = await asyncio.wait(task_list, timeout=None)
    result = []
    # 得到执行结果
    for done_task in done:
        result.extend(done_task.result())
        # print(f"{time.time()} 得到执行结果 {done_task.result()}")
    print(result)
    return result


if __name__ == '__main__':
    start_time = time.time()

    main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_async_bridge_erc20())

    print("总耗时: ", time.time() - start_time)
