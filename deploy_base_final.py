"""Deploy WTC to Base Mainnet"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

# 1. Update wbank_web3.py config
print('[1/6] Updating config to Base Mainnet...')
w = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

w = w.replace('WTC_CHAIN_ID = 11155111', 'WTC_CHAIN_ID = 8453')
w = w.replace('WTC_CHAIN_ID = 97', 'WTC_CHAIN_ID = 8453')
w = w.replace('WTC_CHAIN_ID = 1', 'WTC_CHAIN_ID = 8453')

w = w.replace('"network": "Sepolia Testnet"', '"network": "Base Mainnet"')
w = w.replace('"network": "BSC Testnet"', '"network": "Base Mainnet"')
w = w.replace('"network": "Ethereum Mainnet"', '"network": "Base Mainnet"')

# Update all RPC URLs to Base
old_rpcs = [
    'https://ethereum-sepolia.publicnode.com',
    'https://data-seed-prebsc-1-s1.binance.org:8545',
    'https://rpc.ankr.com/eth',
    'https://eth.llamarpc.com',
    'https://ethereum-rpc.publicnode.com'
]
for rpc in old_rpcs:
    w = w.replace(rpc, 'https://mainnet.base.org')

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w)
print('  [OK] Config updated to Base Mainnet')

# 2. Read deployer key
print('\n[2/6] Loading deployer wallet...')
pk = ''
with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]

deployer = Account.from_key(pk)
print(f'  Deployer: {deployer.address}')

w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org', request_kwargs={'timeout': 60}))
print(f'  Connected: {w3.is_connected()}, Block: {w3.eth.block_number}')

bal = w3.eth.get_balance(deployer.address)
print(f'  Balance: {w3.from_wei(bal, "ether")} ETH')

if bal < 100000000000000:
    print('  [ERROR] Need at least 0.0001 ETH')
    sys.exit(1)

# 3. Compile
print('\n[3/6] Compiling contracts...')
from solcx import compile_files, install_solc
install_solc('0.8.20')

cd = 'E:\\wbank\\contracts'
compiled = compile_files(
    [os.path.join(cd, 'WTC.sol'), os.path.join(cd, 'WTCBridge.sol')],
    solc_version='0.8.20',
    output_values=['abi', 'bin']
)

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

# 4. Deploy WTC
print('\n[4/6] Deploying WTC Token to Base...')
gp = w3.eth.gas_price
print(f'  Gas price: {w3.from_wei(gp, "gwei")} Gwei')

WTC = w3.eth.contract(abi=wtc_info['abi'], bytecode=wtc_info['bin'])
nonce = w3.eth.get_transaction_count(deployer.address)
tx = WTC.constructor().build_transaction({
    'from': deployer.address, 'nonce': nonce,
    'gas': 2000000, 'gasPrice': gp, 'chainId': 8453
})

cost_est = tx['gas'] * tx['gasPrice']
print(f'  Estimated cost: {w3.from_wei(cost_est, "ether")} ETH')

signed = deployer.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f'  TX: {tx_hash.hex()}')

receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
wtc_addr = receipt.contractAddress
print(f'  ✅ WTC deployed: {wtc_addr}')

# 5. Deploy Bridge
bridge_addr = None
if bridge_info:
    print('\n[5/6] Deploying Bridge...')
    nonce2 = w3.eth.get_transaction_count(deployer.address)
    BR = w3.eth.contract(abi=bridge_info['abi'], bytecode=bridge_info['bin'])
    tx2 = BR.constructor(wtc_addr).build_transaction({
        'from': deployer.address, 'nonce': nonce2,
        'gas': 2000000, 'gasPrice': gp, 'chainId': 8453
    })
    signed2 = deployer.sign_transaction(tx2)
    tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
    print(f'  TX: {tx_hash2.hex()}')
    receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2, timeout=120)
    bridge_addr = receipt2.contractAddress
    print(f'  ✅ Bridge deployed: {bridge_addr}')

    # Configure bridge
    nonce3 = w3.eth.get_transaction_count(deployer.address)
    wtc = w3.eth.contract(address=wtc_addr, abi=wtc_info['abi'])
    if wtc.functions.bridgeAddress().call() != bridge_addr:
        tx3 = wtc.functions.setBridge(bridge_addr).build_transaction({
            'from': deployer.address, 'nonce': nonce3,
            'gas': 50000, 'gasPrice': gp, 'chainId': 8453
        })
        signed3 = deployer.sign_transaction(tx3)
        w3.eth.send_raw_transaction(signed3.raw_transaction)
        print('  ✅ Bridge configured')

# 6. Update wbank_web3.py with real address
print('\n[6/6] Updating wbank_web3.py...')
wbank_w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
wbank_w3 = wbank_w3.replace(
    'WTC_CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000"',
    f'WTC_CONTRACT_ADDRESS = "{wtc_addr}"'
)
open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(wbank_w3)
print(f'  ✅ WTC address updated: {wtc_addr}')

# Save artifacts
os.makedirs(os.path.join(cd, 'deployments'), exist_ok=True)
with open(os.path.join(cd, 'deployments', 'base-mainnet.json'), 'w') as f:
    json.dump({'network': 'base', 'chain_id': 8453, 'wtc': {'address': wtc_addr}, 'bridge': {'address': bridge_addr or ''}}, f, indent=2)

# Send some WTC to user's wallet
print(f'\n  Sending WTC to user wallet...')
user_wallet = '0xdffA9CFE9FFA749Fd93883c587193381263AA59c'
min_abi = json.loads('[{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=min_abi)

nonce4 = w3.eth.get_transaction_count(deployer.address)
tx4 = c.functions.transfer(Web3.to_checksum_address(user_wallet), 50000 * 10**18).build_transaction({
    'from': deployer.address, 'nonce': nonce4,
    'gas': 100000, 'gasPrice': w3.eth.gas_price, 'chainId': 8453
})
signed4 = deployer.sign_transaction(tx4)
tx_hash4 = w3.eth.send_raw_transaction(signed4.raw_transaction)
receipt4 = w3.eth.wait_for_transaction_receipt(tx_hash4, timeout=120)
print(f'  ✅ Sent 50,000 WTC to user: {receipt4.status}')

# Done
print(f'\n📊 Basescan: https://basescan.org/address/{wtc_addr}')
print(f'💰 Remaining ETH: {w3.from_wei(w3.eth.get_balance(deployer.address), "ether")}')
print('Restart server now')
