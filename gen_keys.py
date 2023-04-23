#!/usr/bin/python3

from algosdk import mnemonic
from algosdk import account
from web3 import Web3


w3 = Web3()
w3.eth.account.enable_unaudited_hdwallet_features()


def get_algo_keys():
    
    # TODO: Generate or read (using the mnemonic secret) 
    # the algorand public/private keys
    algo_mnemonic = 'avocado annual fluid unlock crowd obey limb eye lunar cliff exile erosion original doctor robot usage nest monitor popular excess medal company cheap able raise'
    algo_sk = mnemonic.to_private_key(algo_mnemonic)
    algo_pk = mnemonic.to_public_key(algo_mnemonic)

    return algo_sk, algo_pk


def get_eth_keys(filename = "eth_mnemonic.txt"):
    w3 = Web3()
    
    # TODO: Generate or read (using the mnemonic secret) 
    # the ethereum public/private keys
    eth_mnemonic = 'gauge inner material time surround scan job security pitch gallery carbon domain'
    acct = w3.eth.account.from_mnemonic(eth_mnemonic)
    eth_pk = acct._address
    eth_sk = acct._private_key
    return eth_sk, eth_pk
