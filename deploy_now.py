"""Simple deploy script - reads key from .env"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')

# Read private key from .env
pk = ''
for env_path in ['E:\\wbank\\.env', 'E:\\wbank\\contracts\\.env']:
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('DEPLOYER_PRIVATE_KEY='):
                    pk = line.split('=', 1)[1].strip()
                    break
    except:
        pass

if not pk:
    print('[ERROR] No private key found')
    sys.exit(1)

if pk.startswith('0x'):
    pk = pk[2:]

print(f'[OK] Private key loaded ({len(pk)} hex chars)')

from eth_account import Account
Account.enable_unaudited_hdwallet_features()
deployer = Account.from_key(pk)
deployer_address = deployer.address
print(f'[OK] Deployer address: {deployer_address}')

from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))
print(f'[OK] Connected to Sepolia (block {w3.eth.block_number})')

bal = w3.eth.get_balance(deployer_address)
print(f'[OK] Balance: {w3.from_wei(bal, "ether")} ETH')

if bal < 10000000000000000:
    print(f'[ERROR] Need at least 0.01 ETH. Send to: {deployer_address}')
    sys.exit(1)

# Compile
from solcx import compile_files, install_solc
install_solc('0.8.20')

cd = 'E:\\wbank\\contracts'
compiled = compile_files(
    [os.path.join(cd, 'WTC.sol'), os.path.join(cd, 'WTCBridge.sol')],
    solc_version='0.8.20',
    output_values=['abi', 'bin']
)

# Find WTC contract
wtc_info = None
bridge_info = None
for path, info in compiled.items():
    if 'WTC.sol' in path and 'Bridge' not in path:
        wtc_info = info
    elif 'Bridge' in path:
        bridge_info = info

if not wtc_info:
    print('[ERROR] WTC contract not found')
    sys.exit(1)

# Deploy WTC
print('\n=== Deploying WTC Token ===')
nonce = w3.eth.get_transaction_count(deployer_address)
gas_price = w3.eth.gas_price
print(f'Gas price: {w3.from_wei(gas_price, "gwei")} Gwei')

WTC = w3.eth.contract(abi=wtc_info['abi'], bytecode=wtc_info['bin'])
tx = WTC.constructor().build_transaction({
    'from': deployer_address,
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': gas_price,
    'chainId': 11155111
})
cost_est = tx['gas'] * tx['gasPrice']
print(f'Estimated cost: {w3.from_wei(cost_est, "ether")} ETH')

signed = deployer.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f'TX: {tx_hash.hex()}')
receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
wtc_addr = receipt.contractAddress
print(f'✅ WTC Token deployed: {wtc_addr}')

# Deploy Bridge
bridge_addr = None
if bridge_info:
    print('\n=== Deploying WTCBridge ===')
    nonce2 = w3.eth.get_transaction_count(deployer_address)
    BR = w3.eth.contract(abi=bridge_info['abi'], bytecode=bridge_info['bin'])
    tx2 = BR.constructor(wtc_addr).build_transaction({
        'from': deployer_address,
        'nonce': nonce2,
        'gas': 2000000,
        'gasPrice': gas_price,
        'chainId': 11155111
    })
    signed2 = deployer.sign_transaction(tx2)
    tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
    print(f'TX: {tx_hash2.hex()}')
    receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2, timeout=120)
    bridge_addr = receipt2.contractAddress
    print(f'✅ Bridge deployed: {bridge_addr}')

    # Configure bridge in WTC
    print('\n=== Configuring Bridge ===')
    nonce3 = w3.eth.get_transaction_count(deployer_address)
    wtc = w3.eth.contract(address=wtc_addr, abi=wtc_info['abi'])
    tx3 = wtc.functions.setBridge(bridge_addr).build_transaction({
        'from': deployer_address,
        'nonce': nonce3,
        'gas': 50000,
        'gasPrice': gas_price,
        'chainId': 11155111
    })
    signed3 = deployer.sign_transaction(tx3)
    tx_hash3 = w3.eth.send_raw_transaction(signed3.raw_transaction)
    receipt3 = w3.eth.wait_for_transaction_receipt(tx_hash3, timeout=60)
    print('✅ Bridge configured in WTC')

# Save deployment info
artifacts = {
    'network': 'sepolia',
    'chain_id': 11155111,
    'wtc': {'address': wtc_addr},
    'bridge': {'address': bridge_addr or ''}
}
os.makedirs(os.path.join(cd, 'deployments'), exist_ok=True)
with open(os.path.join(cd, 'deployments', 'sepolia.json'), 'w') as f:
    json.dump(artifacts, f, indent=2)
print(f'\n📁 Saved to: {cd}\\deployments\\sepolia.json')

# Update wbank_web3.py
w3_path = 'E:\\wbank\\wbank_web3.py'
wb3 = open(w3_path, 'r', encoding='utf-8').read()
wb3 = wb3.replace(
    'WTC_CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000"',
    f'WTC_CONTRACT_ADDRESS = "{wtc_addr}"'
)
open(w3_path, 'w', encoding='utf-8').write(wb3)
print(f'✅ wbank_web3.py updated with WTC address')

print(f'\n📊 Explorer: https://sepolia.etherscan.io/address/{wtc_addr}')
print(f'🌉 Bridge: {bridge_addr or "N/A"}')
print('\n=== DONE ===')
