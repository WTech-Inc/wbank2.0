import sys
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
tx = 'e56babbc189febec7b162937f25e74d95bd592430d6ebf0c2ceb16184e07a1c0'
try:
    r = w3.eth.get_transaction_receipt(tx)
    print('ON-CHAIN! Status:', r.status)
    print('Block:', r.blockNumber)
except Exception as e:
    print('NOT on-chain:', str(e)[:80])
