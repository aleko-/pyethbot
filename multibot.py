from robit import Robit
import random
import string
import os
import getpass

# Ropsten testnet
# from web3 import Web3
# ropsten = Web3.HTTPProvider('https://ropsten.infura.io')
# w3 = Web3(ropsten)

# Mainnet
from web3.auto.infura import w3

class MultiBot:
    def __init__(self):
        self.accounts = []

    def create_account(self, name, dir_, password, load=True):
        chars = string.ascii_letters + string.digits + string.punctuation
        entropy = ''.join([random.choice(chars) for _ in range(15)])

        fpath = './accs/{}/'.format(dir_)
        if not os.path.isdir(fpath):
            os.mkdir(fpath)
        name = dir_ + '/' + name

        r = Robit()
        r.create_account(entropy)
        r.encrypt_account(fname=name, password=password)

        if load:
            self.accounts.append(r)

        return r.address

    def create_accounts(self, n, dir_, password, verbose=True):
        """
        create n accounts in the specified directory
        """
        for i in range(1, n+1):
            name = 'acc_{}'.format(i)
            addr = self.create_account(name, dir_, password)

            if verbose:
                print("{} : {}".format(name, addr))

    def load_accounts(self, dir_, password=None):
        password = getpass.getpass() if not password else password
        for account in os.listdir('./accs/{}'.format(dir_)):
            print("Loading account {}".format(account))
            fpath = dir_ + '/' + account
            r = Robit()
            r.load_account(fpath, password)
            self.accounts.append(r)

    def distribute_eth(self,
                       primary=None,
                       gas_price=7,
                       gas_limit=21000,
                       chainId=1):
        """
        Distribute from primary wallet to all other wallets.
        Even distribution between all wallets.

        Change chainId if using testnet:
        2: Morden
        3: Ropsten
        4: Rinkeby
        42: Kovan
        """

        # Determine primary account
        if not primary:
            balances = [w3.eth.getBalance(account.address)
                              for account in self.accounts]
            idx = balances.index(max(balances))
            primary = self.accounts[idx]

        # Calculate eth value to send and gas price
        total_eth = w3.eth.getBalance(primary.address)
        gas_cost = w3.toWei((gas_price * gas_limit), 'gwei')
        eth_to_pay = (total_eth - gas_cost) / len(self.accounts)

        # Return if gas is more expensive than eth to send
        if (total_eth - gas_cost) < (gas_cost * len(self.accounts)):
            print("Not enough ETH to cover gas cost")
            return

        # Iterate over accounts in directory and send eth
        tx_count = 0
        for account in self.accounts:
            if primary.address == account.address:
                continue

            # Rounding error may not leave enough eth for the last tx
            primary_balance = w3.eth.getBalance(primary.address)
            if eth_to_pay > (primary_balance - gas_cost):
                eth_to_pay = primary_balance - gas_cost

            nonce = primary.get_nonce() + tx_count
            tx = primary.generate_transaction(account.address,
                                              eth_to_pay,
                                              gas_price,
                                              gas_limit,
                                              nonce=nonce,
                                              chainId=chainId)

            signed = primary.sign_transaction(tx)
            primary.send_transaction(signed)

            tx_count += 1
            print(tx)


    def consolidate_eth(self,
                        to=None,
                        gas_price=7,
                        gas_limit=21000,
                        chainId=1):
        """
        Send eth from all accounts in one directory to the primary account
        """
        to = self.accounts[0].address if not to else to

        for account in self.accounts:
            if to == account.address or w3.eth.getBalance(account.address)==0:
                continue

            # Determine remaining balance after gas cost
            gas_cost = w3.toWei((gas_price * gas_limit), 'gwei')
            eth = w3.eth.getBalance(account.address) - gas_cost

            tx = account.generate_transaction(to,
                                              eth,
                                              gas_price,
                                              gas_limit,
                                              chainId=chainId)
            signed = account.sign_transaction(tx)
            account.send_transaction(signed)
            print(tx)

    def show_balances(self):
        for account in self.accounts:
            print(account.get_balance())


if __name__=='__main__':
    mb = MultiBot()

