import sys
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))
tx_hash = '0xe219848233380a07c5f8b40f9c9dbe10c08c8ef7e2a5ef2090012a8aacb897d6'

try:
    tx = w3.eth.get_transaction(tx_hash)
    print(f'✅ REAL TX!')
    print(f'From: {tx["from"]}')
    print(f'To: {tx["to"]}')
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    print(f'Status: {"✅" if receipt.status == 1 else "❌"}')
    print(f'Block: {receipt.blockNumber}')
    print(f'Gas: {receipt.gasUsed}')
except:
    print('❌ Not on-chain (simulated)')

# Check user balance
user = '0x53A081aeedD98D82ef29ed93818a501E2CeD2209'
print(f'\nUser ETH: {w3.from_wei(w3.eth.get_balance(user), "ether")}')

import json
abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address('0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'), abi=abi)
wtc = c.functions.balanceOf(Web3.to_checksum_address(user)).call()
print(f'User WTC on-chain: {wtc / 10**18:,.2f}')
