"""Resend ETH with higher gas to replace stuck tx"""
import sys, json, time
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com', request_kwargs={'timeout': 120}))

user_addr = '0x53A081aeedD98D82ef29ed93818a501E2CeD2209'

# Load key
pk = ''
with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]
deployer = Account.from_key(pk)
deployer_addr = deployer.address

# Check current state
nonce = w3.eth.get_transaction_count(deployer_addr)
print(f'Deployer nonce: {nonce}')
print(f'Deployer ETH: {w3.from_wei(w3.eth.get_balance(deployer_addr), "ether")}')

# Check if user already has ETH
user_eth = w3.eth.get_balance(user_addr)
print(f'User ETH: {w3.from_wei(user_eth, "ether")}')

if user_eth == 0:
    # Send ETH with higher gas price to replace stuck tx
    gp = w3.eth.gas_price
    print(f'Gas price: {w3.from_wei(gp, "gwei")} Gwei')

    # Use nonce 3 (same as stuck tx) with 50% higher gas to replace
    tx = {
        'to': user_addr,
        'value': w3.to_wei(0.02, 'ether'),
        'gas': 21000,
        'gasPrice': int(gp * 1.5),
        'nonce': nonce,  # Current nonce (might be 4 or 5)
        'chainId': 11155111
    }
    signed = deployer.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f'ETH TX: {tx_hash.hex()}')
    print('Waiting for confirmation (up to 120s)...')

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    print(f'ETH TX status: {"✅" if receipt.status == 1 else "❌"}')
else:
    print('Skipping ETH - user already has some')

# Send WTC regardless
wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
abi = json.loads('[{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=abi)

bal_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
c_bal = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=bal_abi)
user_wtc = c_bal.functions.balanceOf(Web3.to_checksum_address(user_addr)).call()

if user_wtc == 0:
    nonce2 = w3.eth.get_transaction_count(deployer_addr)
    gp2 = w3.eth.gas_price
    tx2 = c.functions.transfer(user_addr, 50000 * 10**18).build_transaction({
        'from': deployer_addr, 'nonce': nonce2,
        'gas': 150000, 'gasPrice': gp2,
        'chainId': 11155111
    })
    signed2 = deployer.sign_transaction(tx2)
    tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
    print(f'WTC TX: {tx_hash2.hex()}')
    print('Waiting for confirmation (up to 120s)...')
    try:
        receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2, timeout=120)
        print(f'WTC TX status: {"✅" if receipt2.status == 1 else "❌"}')
    except:
        print('WTC TX time out, checking later...')

# Final check
time.sleep(5)
user_eth = w3.eth.get_balance(user_addr)
user_wtc = c_bal.functions.balanceOf(Web3.to_checksum_address(user_addr)).call()
print(f'\n=== Results ===')
print(f'User ETH: {w3.from_wei(user_eth, "ether")}')
print(f'User WTC: {user_wtc / 10**18:,.0f}')
if user_eth > 0 and user_wtc > 0:
    print('✅ User wallet ready for real on-chain WTC transfers!')
