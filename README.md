# pyethbot
----

pyethbot abstracts the web3py library to allows for quicker wallet management.

# current functionality
----

### Robit.py
- Create a wallet
- Encrypt/Decrypt wallet
- Get balance
- Generate, sign, and send transactions

### Multibot.py
- Create/load multiple wallets at once
- Distribute ether evenly amongst all wallets
- Consolidate ether from wallets into one main wallet
- Show balances on all wallets

# example usage
----
    >>> from multibot import MultiBot
    >>> mb=MultiBot()
    >>> mb.create_accounts(n=5, dir_='testing', password='testing')
    acc_1 : 0x843c03F8eEc7B70f1F7B95CA49dBfe90f86ED7B4
    acc_2 : 0x72cf0DAB328147dB83FD5604b32e8AC0A9f6a81E
    acc_3 : 0xFCC7b8A5Aa947EcD2058f038A63c5627c6225c73
    acc_4 : 0x9Ae76974D7a4223d5279FdA7113e876e900057A7
    acc_5 : 0x0C68b3b44758Bd006C11C4c0F28b09B412909316

To load these accounts in a new session:

    >>> from multibot import MultiBot
    >>> mb=MultiBot()
    >>> mb.load_accounts('testing', password='testing')
    Loading account acc_4
    Loading account acc_3
    Loading account acc_2
    Loading account acc_5
    Loading account acc_1

Load one of the addresses with ether:

    >>> mb.show_balances()
    0.0
    0.0
    0.0
    0.0
    1.05010391

Distribute ether:

    >>> mb.distribute_eth()
    >>> mb.show_balances()
    0.209991382
    0.209991382
    0.209991382
    0.209991382
    0.209550382

Consolidate ether:

    >>> mb.consolidate_eth()
    >>> mb.show_balances()
    1.04892791
    0.0
    0.0
    0.0
    0.0
