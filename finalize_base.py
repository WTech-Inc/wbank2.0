"""Finalize: configure bridge + send WTC + sync DB"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()
from solcx import compile_files, install_solc
install_solc('0.8.20')

cd = 'E:\\wbank\\contracts'
wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
bridge_addr = '0x028D0e9E691aD87980c5AdF3c3951fe5A482874B'

w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org', request_kwargs={'timeout': 60}))

pk = ''
with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]
deployer = Account.from_key(pk)

# Compile WTC for ABI
compiled = compile_files([os.path.join(cd, 'WTC.sol')], solc_version='0.8.20', output_values=['abi'])
wtc_info = [v for k,v in compiled.items() if 'WTC' in k and 'Bridge' not in k][0]
wtc = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=wtc_info['abi'])

nonce = w3.eth.get_transaction_count(deployer.address)
print(f'Nonce: {nonce}')
print(f'Balance: {w3.from_wei(w3.eth.get_balance(deployer.address), "ether")} ETH')

# 1. Configure bridge
print('\n1. Configuring Bridge...')
if wtc.functions.bridgeAddress().call() != bridge_addr:
    tx = wtc.functions.setBridge(Web3.to_checksum_address(bridge_addr)).build_transaction({
        'from': deployer.address, 'nonce': nonce, 'gas': 50000,
        'gasPrice': w3.eth.gas_price, 'chainId': 8453
    })
    signed = deployer.sign_transaction(tx)
    h = w3.eth.send_raw_transaction(signed.raw_transaction)
    r = w3.eth.wait_for_transaction_receipt(h, timeout=60)
    print(f'  Bridge configured: {"OK" if r.status == 1 else "FAIL"}')
    nonce += 1
else:
    print('  Already configured')

# 2. Send WTC to user
print('\n2. Sending 50000 WTC to user...')
user = '0xdffA9CFE9FFA749Fd93883c587193381263AA59c'
tx2 = wtc.functions.transfer(Web3.to_checksum_address(user), 50000 * 10**18).build_transaction({
    'from': deployer.address, 'nonce': nonce, 'gas': 100000,
    'gasPrice': w3.eth.gas_price, 'chainId': 8453
})
signed2 = deployer.sign_transaction(tx2)
h2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
r2 = w3.eth.wait_for_transaction_receipt(h2, timeout=120)
print(f'  WTC sent: {"OK" if r2.status == 1 else "FAIL"}')
nonce += 1

# 3. Send 0.001 ETH to user for gas
print('\n3. Sending 0.001 ETH to user for gas...')
tx3 = {'to': user, 'value': w3.to_wei(0.001, 'ether'), 'gas': 21000,
    'gasPrice': w3.eth.gas_price, 'nonce': nonce, 'chainId': 8453}
signed3 = deployer.sign_transaction(tx3)
h3 = w3.eth.send_raw_transaction(signed3.raw_transaction)
r3 = w3.eth.wait_for_transaction_receipt(h3, timeout=60)
print(f'  ETH sent: {"OK" if r3.status == 1 else "FAIL"}')

# 4. Update wbank_web3.py
print('\n4. Updating wbank_web3.py...')
wb3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
wb3 = wb3.replace('WTC_CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000"', f'WTC_CONTRACT_ADDRESS = "{wtc_addr}"')
open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(wb3)
print('  OK')

# 5. Sync DB balance
print('\n5. Syncing DB balance...')
import psycopg2
conn = psycopg2.connect(database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()
cur.execute(f"UPDATE wbankwallet SET balance='50000' WHERE username='wangtry'")
conn.commit()
cur.execute("UPDATE wbankwallet SET eth_address=%s WHERE username='wangtry'", (user,))
cur.execute("UPDATE wbankwallet SET eth_key_encrypted='external_wallet_no_key' WHERE username='wangtry'")
conn.commit()
conn.close()
print('  OK - DB: 50000 WTC')

# Save artifacts
os.makedirs(os.path.join(cd, 'deployments'), exist_ok=True)
with open(os.path.join(cd, 'deployments', 'base-mainnet.json'), 'w') as f:
    json.dump({'network': 'base', 'chain_id': 8453, 'wtc': {'address': wtc_addr}, 'bridge': {'address': bridge_addr}}, f, indent=2)

remaining = w3.eth.get_balance(deployer.address)
print(f'\n📊 Basescan: https://basescan.org/address/{wtc_addr}')
print(f'💰 Remaining: {w3.from_wei(remaining, "ether")} ETH')
print('Restart server now')
