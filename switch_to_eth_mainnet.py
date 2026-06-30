"""Switch WTC config from BSC to Ethereum Mainnet"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Replace BSC Testnet references with Ethereum Mainnet
w3 = w3.replace(
    'WTC_CHAIN_ID = 97',
    'WTC_CHAIN_ID = 1'
)
w3 = w3.replace(
    'WTC_RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545"',
    'WTC_RPC_URL = "https://eth.llamarpc.com"'
)
w3 = w3.replace(
    'BSC_RPC = "https://data-seed-prebsc-1-s1.binance.org:8545"',
    'ETH_RPC = "https://eth.llamarpc.com"'
)
w3 = w3.replace(
    'w3 = Web3(Web3.HTTPProvider(BSC_RPC))',
    'w3 = Web3(Web3.HTTPProvider(ETH_RPC))'
)
w3 = w3.replace(
    '"network": "BSC Testnet"',
    '"network": "Ethereum Mainnet"'
)

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

# Verify
print('Updated config:')
for line in w3.split('\n'):
    if 'CHAIN_ID' in line or 'RPC_URL' in line or 'network' in line:
        print(f'  {line.strip()}')

# Also update deploy script default
deploy = open('E:\\wbank\\contracts\\deploy_contracts.py', 'r', encoding='utf-8').read()
deploy = deploy.replace(
    'net_name = sys.argv[1] if len(sys.argv)>1 else "bsc-testnet"',
    'net_name = sys.argv[1] if len(sys.argv)>1 else "eth-mainnet"'
)

# Add eth-mainnet to networks if not already there
if 'eth-mainnet' not in deploy:
    # Add it before the closing brace
    eth_net = """,
    "eth-mainnet": {"chain_id": 1, "rpc": "https://eth.llamarpc.com", "explorer": "https://etherscan.io", "currency": "ETH", "name": "Ethereum Mainnet"}
}"""
    deploy = deploy.rstrip('}') + eth_net

open('E:\\wbank\\contracts\\deploy_contracts.py', 'w', encoding='utf-8').write(deploy)
print('\n[OK] Deploy script updated for Ethereum Mainnet')

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')

print('\n=== Restart server ===')
