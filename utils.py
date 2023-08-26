# @Time : 8/26/23 10:54 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : utils.py
from web3 import Web3, HTTPProvider, AsyncHTTPProvider, AsyncWeb3
from config import Config

class Web3Client(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Web3Client, cls).__new__(cls)
            cls._web3 = Web3(HTTPProvider(Config.ETH_PROVIDER_URL.value))
            cls._web3.is_connected()
        return cls._instance

    def get_web3(self):
        return self._web3

class AsyncWeb3Client(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AsyncWeb3Client, cls).__new__(cls)
            cls._web3 = AsyncWeb3(AsyncHTTPProvider(Config.ETH_PROVIDER_URL.value))
            cls._web3.is_connected()
        return cls._instance

    def get_web3(self):
        return self._web3