"""Fix RPC and deploy config for Ethereum Mainnet"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Fix RPC
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
w3 = w3.replace('eth.llamarpc.com', 'rpc.ankr.com/eth')
open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

# Fix deploy script
d = open('E:\\wbank\\contracts\\deploy_contracts.py', 'r', encoding='utf-8').read()
if '"eth-mainnet"' not in d:
    eth_entry = ',\n    "eth-mainnet": {"chain_id": 1, "rpc": "https://rpc.ankr.com/eth", "explorer": "https://etherscan.io", "currency": "ETH", "name": "Ethereum Mainnet"}\n}'
    d = d.rstrip('}') + eth_entry
    open('E:\\wbank\\contracts\\deploy_contracts.py', 'w', encoding='utf-8').write(d)

print('[OK] RPC: Ankr Ethereum')
print('[OK] Deploy: eth-mainnet added')

# Verify connection
import subprocess
result = subprocess.run([sys.executable, '-c', '''
from web3 import Web3
w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth"))
print(f"ETH Mainnet connected: {w3.is_connected()}")
print(f"Block: {w3.eth.block_number}")
'''], capture_output=True, text=True, timeout=15)
print(f'[TEST] {result.stdout.strip()[:100]}')
if result.stderr:
    print(f'[WARN] {result.stderr[:200]}')
