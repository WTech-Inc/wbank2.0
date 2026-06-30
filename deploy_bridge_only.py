"""Deploy Bridge only (WTC already deployed)"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
print(f'WTC Token: {wtc_addr}')

w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org', request_kwargs={'timeout': 60}))
print(f'Connected: {w3.is_connected()}, Block: {w3.eth.block_number}')

pk = ''
with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]

deployer = Account.from_key(pk)
print(f'Deployer: {deployer.address}')
print(f'Balance: {w3.from_wei(w3.eth.get_balance(deployer.address), "ether")} ETH')
print(f'Nonce: {w3.eth.get_transaction_count(deployer.address)}')

# Deploy Bridge
from solcx import compile_files, install_solc
install_solc('0.8.20')
cd = 'E:\\wbank\\contracts'
compiled = compile_files([os.path.join(cd, 'WTCBridge.sol')], solc_version='0.8.20', output_values=['abi', 'bin'])

bridge_info = None
for path, info in compiled.items():
    if 'Bridge' in path:
        bridge_info = info
        break

if not bridge_info:
    print('Bridge contract not found')
    sys.exit(1)

print('\n=== Deploying Bridge ===')
gp = w3.eth.gas_price
nonce = w3.eth.get_transaction_count(deployer.address)
print(f'Gas: {w3.from_wei(gp, "gwei")} Gwei, Nonce: {nonce}')

BR = w3.eth.contract(abi=bridge_info['abi'], bytecode=bridge_info['bin'])
tx = BR.constructor(wtc_addr).build_transaction({
    'from': deployer.address, 'nonce': nonce,
    'gas': 2000000, 'gasPrice': gp, 'chainId': 8453
})

signed = deployer.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f'TX: {tx_hash.hex()}')
receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
bridge_addr = receipt.contractAddress
print(f'✅ Bridge deployed: {bridge_addr}')

# Configure bridge
print('\n=== Configuring Bridge ===')
nonce2 = w3.eth.get_transaction_count(deployer.address)
wtc = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=bridge_info['abi'])
tx2 = wtc.functions.setBridge(bridge_addr).build_transaction({
    'from': deployer.address, 'nonce': nonce2,
    'gas': 50000, 'gasPrice': w3.eth.gas_price, 'chainId': 8453
})
signed2 = deployer.sign_transaction(tx2)
tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
print(f'Config TX: {tx_hash2.hex()}')
receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2, timeout=60)
print(f'Status: {"✅" if receipt2.status == 1 else "❌"}')

# Send WTC to user
print('\n=== Sending WTC to user ===')
nonce3 = w3.eth.get_transaction_count(deployer.address)
user_addr = '0xdffA9CFE9FFA749Fd93883c587193381263AA59c'
import json
abi = json.loads('[{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=abi)
tx3 = c.functions.transfer(Web3.to_checksum_address(user_addr), 50000 * 10**18).build_transaction({
    'from': deployer.address, 'nonce': nonce3,
    'gas': 100000, 'gasPrice': w3.eth.gas_price, 'chainId': 8453
})
signed3 = deployer.sign_transaction(tx3)
tx_hash3 = w3.eth.send_raw_transaction(signed3.raw_transaction)
print(f'WTC TX: {tx_hash3.hex()}')
receipt3 = w3.eth.wait_for_transaction_receipt(tx_hash3, timeout=120)
print(f'Status: {"✅" if receipt3.status == 1 else "❌"}')
print('✅ 50,000 WTC sent to user')

# Send some ETH to user for gas
print('\n=== Sending ETH to user for gas ===')
nonce4 = w3.eth.get_transaction_count(deployer.address)
tx4 = {
    'to': user_addr,
    'value': w3.to_wei(0.001, 'ether'),
    'gas': 21000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce4,
    'chainId': 8453
}
signed4 = deployer.sign_transaction(tx4)
tx_hash4 = w3.eth.send_raw_transaction(signed4.raw_transaction)
print(f'ETH TX: {tx_hash4.hex()}')
receipt4 = w3.eth.wait_for_transaction_receipt(tx_hash4, timeout=60)
print(f'Status: {"✅" if receipt4.status == 1 else "❌"}')

# Save
os.makedirs(os.path.join(cd, 'deployments'), exist_ok=True)
with open(os.path.join(cd, 'deployments', 'base-mainnet.json'), 'w') as f:
    json.dump({'network': 'base', 'chain_id': 8453, 'wtc': {'address': wtc_addr}, 'bridge': {'address': bridge_addr}}, f, indent=2)

print(f'\n📊 Basescan: https://basescan.org/address/{wtc_addr}')
print(f'🚀 Bridge: {bridge_addr}')
print(f'💰 Remaining: {w3.from_wei(w3.eth.get_balance(deployer.address), "ether")} ETH')
