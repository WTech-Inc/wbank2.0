import sys
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))

# Check recent send tx
tx_hash = '0x13bb30a3ec2483c6737b04d6d90cb90535e8853324e5330eda63f81613b9d588'
try:
    tx = w3.eth.get_transaction(tx_hash)
    print(f'✅ REAL TX found!')
    print(f'From: {tx["from"]}')
    print(f'To: {tx["to"]}')
    print(f'Value: {w3.from_wei(tx["value"], "ether")} ETH')

    receipt = w3.eth.get_transaction_receipt(tx_hash)
    print(f'Status: {"✅ Success" if receipt.status == 1 else "❌ Failed"}')
    print(f'Block: {receipt.blockNumber}')
    print(f'Gas used: {receipt.gasUsed}')
except:
    print('❌ TX not found on-chain (simulated hash)')

# Check user balances
user = '0x53A081aeedD98D82ef29ed93818a501E2CeD2209'
print(f'\nUser wallet: {user}')
print(f'ETH: {w3.from_wei(w3.eth.get_balance(user), "ether")}')
