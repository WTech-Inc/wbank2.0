import sys
sys.stdout.reconfigure(encoding='utf-8')

from web3 import Web3

rpcs = [
    'https://eth.llamarpc.com',
    'https://rpc.ankr.com/eth',
    'https://ethereum-rpc.publicnode.com',
    'https://1rpc.io/eth',
    'https://cloudflare-eth.com'
]

for rpc in rpcs:
    try:
        w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 10}))
        c = w3.is_connected()
        b = w3.eth.block_number if c else 0
        print(f'{rpc}: connected={c}, block={b}')
    except Exception as e:
        print(f'{rpc}: ERROR {str(e)[:80]}')
