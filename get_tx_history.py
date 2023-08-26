# @Time : 8/25/23 4:37 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : get_tx_history.py.py
import json
from typing import List
import ctc
import requests
import urllib3
import web3
import pprint
from utils import Web3Client
from config import Config

client = Web3Client()
w3 = client.get_web3()


class NaturalETH(object):

    def find_all_transactions(self, sender: str, from_block: int = Config.ETH_AUTO_SYNC_FROM_BLOCK.value,
                              to_block: int | str = 'latest'):
        ether_custodian_abi = json.loads(Config.ETHER_CUSTODIAN_ABI.value)
        ether_custodian_address = Config.ETHER_CUSTODIAN_ADDRESS.value
        contract = w3.eth.contract(address=ether_custodian_address, abi=ether_custodian_abi)
        contract_filter = contract.events.Deposited.create_filter(
            fromBlock=from_block,
            toBlock=to_block,
            # address=sender_address,
            argument_filters={"sender": sender}
        )
        all_events = contract_filter.get_all_entries()

        # remove recipient startwith aurora，return transactionHash list
        tx_hash_list = [e['transactionHash'].hex() for e in all_events if
                        not e['args']['recipient'].startswith('aurora:')]
        return tx_hash_list


class BridgedETH(object):

    def find_all_transactions(self, sender: str, from_block: int | str = Config.NEAR_AUTO_SYNC_FROM_BLOCK.value,
                              to_block: int | str = 'latest', receive_account: str = Config.AURORA_EVM_ACCOUNT.value):
        # aurora_evm_account = 'aurora'
        # req_url = f"https://mainnet-indexer.ref-finance.com/call-indexer"
        urllib3.disable_warnings()
        rep = requests.get(Config.CALL_INDEXER_API.value, params={
            "from_block": from_block,
            "to_block": to_block,
            "predecessor_account_id": sender,
            "receiver_account_id": receive_account
        },verify=False)
        tx_res = rep.json()
        result = [tx['originated_from_transaction_hash'] for tx in tx_res if tx['args']['method_name'] == 'withdraw']
        return result


class NaturalNEAR(object):

    def find_all_transactions(self, sender: str, from_block: int | str = Config.NEAR_AUTO_SYNC_FROM_BLOCK.value,
                              to_block: int | str = 'latest',
                              receive_account: str = Config.NATIVE_NEAR_LOCKER_ADDRESS.value):
        urllib3.disable_warnings()
        rep = requests.get(Config.CALL_INDEXER_API.value, params={
            "from_block": from_block,
            "to_block": to_block,
            "predecessor_account_id": sender,
            "receiver_account_id": receive_account
        },verify=False)
        tx_res = rep.json()
        result = [tx['originated_from_transaction_hash'] for tx in tx_res if
                  tx['args']['method_name'] == 'migrate_to_ethereum']
        return result


class BridgedNEAR(object):

    def find_all_transactions(self, sender: str,
                              from_block: int = Config.ETH_AUTO_SYNC_FROM_BLOCK.value, to_block: int | str = 'latest'):
        enear_abi = json.loads(Config.E_NEAR_ABI.value)
        enear_address = w3.to_checksum_address(Config.E_NEAR_ADDRESS.value)
        contract = w3.eth.contract(address=enear_address, abi=enear_abi)
        contract_filter = contract.events.TransferToNearInitiated.create_filter(
            fromBlock=from_block,
            toBlock=to_block,
            # address=sender_address,
            argument_filters={"sender": sender}
        )
        all_events = contract_filter.get_all_entries()

        # remove recipient startwith aurora，return transactionHash list
        tx_hash_list = [e['transactionHash'].hex() for e in all_events if
                        not e['args']['accountId'].startswith('aurora:')]
        return tx_hash_list


class NaturalErc20():
    """
    nep141 - erc20
    """

    def find_all_transactions(self, sender: str, erc20_address: str,
                              from_block: int = Config.ETH_AUTO_SYNC_FROM_BLOCK.value, to_block: int | str = 'latest'):
        erc20_locker_abi = json.loads(Config.ERC20_LOCKER_ABI.value)
        erc20_locker_address = w3.to_checksum_address(Config.ERC20_LOCKER_ADDRESS.value)
        contract = w3.eth.contract(address=erc20_locker_address, abi=erc20_locker_abi)
        contract_filter = contract.events.Locked.create_filter(
            fromBlock=from_block,
            toBlock=to_block,
            argument_filters={"sender": sender, "token": erc20_address}
        )
        all_events = contract_filter.get_all_entries()

        # remove recipient startwith aurora，return transactionHash list
        tx_hash_list = [e['transactionHash'].hex() for e in all_events if
                        not e['args']['accountId'].startswith('aurora:')]
        return tx_hash_list


class BridgedNep141():
    """
    nep141 - erc20
    """

    def _get_nep141_address(self, erc20_address):
        nep141Factory = Config.NEAR_TOKEN_FACTORY_ACCOUNT.value

        # remove 0x prefix  and lower
        erc20_addr = w3.to_checksum_address(erc20_address)[2:].lower()
        # 拼接Nep141地址
        nep141_address = f"{erc20_addr}.{nep141Factory}"
        print(nep141_address)
        return nep141_address

    def find_all_transactions(self, sender: str, erc20_address: str,
                              from_block: int = Config.NEAR_AUTO_SYNC_FROM_BLOCK.value, to_block: int | str = 'latest'):
        nep141_address = self._get_nep141_address(erc20_address)

        urllib3.disable_warnings()
        rep = requests.get(Config.CALL_INDEXER_API.value, params={
            "from_block": from_block,
            "to_block": to_block,
            "predecessor_account_id": sender,
            "receiver_account_id": nep141_address
        }, verify=False)
        print(rep.url)
        tx_res = rep.json()
        result = [tx['originated_from_transaction_hash'] for tx in tx_res if
                  tx['args']['method_name'] == 'withdraw']
        return result
