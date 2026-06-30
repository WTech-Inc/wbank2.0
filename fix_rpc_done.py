import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
w3 = w3.replace('rpc.ankr.com/eth', 'ethereum-rpc.publicnode.com')
w3 = w3.replace('eth.llamarpc.com', 'ethereum-rpc.publicnode.com')
open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

# Verify
for line in w3.split('\n'):
    if 'RPC' in line or 'CHAIN' in line or 'network' in line:
        print(line.strip()[:150])

# Test connection
from web3 import Web3
w3_test = Web3(Web3.HTTPProvider('https://ethereum-rpc.publicnode.com', request_kwargs={'timeout': 10}))
print(f'\nConnected: {w3_test.is_connected()}')
if w3_test.is_connected():
    print(f'Block: {w3_test.eth.block_number}')
