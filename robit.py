import json
import getpass
import time
import sys

from eth_account import Account
from eth_account.messages import defunct_hash_message

# Ropsten testnet
# from web3 import Web3
# ropsten = Web3.HTTPProvider('https://ropsten.infura.io')
# w3 = Web3(ropsten)

# Mainnet
from web3.auto.infura import w3

class Robit:
    def __init__(self, account=None):
        if account:
            self.load_account(account)

    def create_account(self, entropy):
        self.account = Account.create(entropy)
        self.pk = self.account.privateKey
        self.address = w3.toChecksumAddress(self.account.address)

    def encrypt_account(self, fname, fpath=None, password=None):
        """
        Encrypt private key and metadata
        """
        fpath = './accs/' + fname if not fpath else fpath
        password = getpass.getpass() if not password else password
        encrypted = Account.encrypt(self.pk, password)
        with open(fpath, 'w') as f:
            f.write(json.dumps(encrypted))

    def decrypt_account(self, fname, fpath=None, password=None):
        """
        Decrypts private key
        """
        fpath = './accs/' + fname if not fpath else fpath
        password = getpass.getpass() if not password else password
        with open(fpath, 'r') as  f:
            encrypted = json.load(f)
            self.pk = Account.decrypt(encrypted, password)

    def load_account(self, fname, password=None):
        self.decrypt_account(fname=fname, password=password)
        self.account = Account.privateKeyToAccount(self.pk)
        self.address = w3.toChecksumAddress(self.account.address)

    def get_balance(self):
        return float(w3.fromWei(w3.eth.getBalance(self.address), 'ether'))

    def get_nonce(self):
        return w3.eth.getTransactionCount(self.address)

    def sign_hash(self, msg, pk):
        msghash = defunct_hash_message(msg)
        return Account.signHash(msghash, pk)

    def generate_transaction(self,
                             to,
                             ether,
                             gas_price,
                             gas_limit,
                             nonce=None,
                             chainId=1,
                             denom='wei'):
        nonce = self.get_nonce() if not nonce else nonce

        value = w3.toWei(ether, denom)
        gasPrice = w3.toWei(gas_price, 'gwei')

        data = {
                 'to'       : w3.toChecksumAddress(to),
                 'from'     : self.address,
                 'value'    : value,
                 'gas'      : gas_limit,
                 'gasPrice' : gasPrice,
                 'nonce'    : nonce,
                 'chainId'  : chainId
                }
        return data

    def sign_transaction(self, tx):
        return Account.signTransaction(tx, self.pk)

    def send_transaction(self, signedtx):
        w3.eth.sendRawTransaction(signedtx.rawTransaction)

    def convert_wei(self, amount, denom):
        return float(w3.fromWei(amount, denom))

