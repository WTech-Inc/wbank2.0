"""Fund user wallet with better RPC"""
import sys, json, time
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

# Use a more reliable RPC for writes
RPC = 'https://rpc.sepolia.org'
w3 = Web3(Web3.HTTPProvider(RPC, request_kwargs={'timeout': 60}))
print(f'Connected: {w3.is_connected()}, Block: {w3.eth.block_number}')

wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
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

# Check if user already has ETH
user_eth = w3.eth.get_balance(user_addr)
if user_eth > 0:
    print(f'\nUser already has {w3.from_wei(user_eth, "ether")} ETH - skipping')
else:
    print(f'\n1. Sending 0.02 SepoliaETH...')
    nonce = w3.eth.get_transaction_count(deployer_addr)
    gp = w3.eth.gas_price
    tx = {
        'to': user_addr,
        'value': w3.to_wei(0.02, 'ether'),
        'gas': 21000,
        'gasPrice': gp,
        'nonce': nonce,
        'chainId': 11155111
    }
    signed = deployer.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f'TX: {tx_hash.hex()}')
    # Wait shorter but check multiple times
    for i in range(30):
        time.sleep(4)
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                print(f'Status: {"✅" if receipt.status == 1 else "❌"}')
                break
        except:
            pass
    else:
        print('⚠️ TX not confirmed yet, but broadcasted')

# Send WTC
print(f'\n2. Sending 50000 WTC...')
abi = json.loads('[{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=abi)

# Check user's WTC balance first
bal_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
c_bal = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=bal_abi)
user_wtc = c_bal.functions.balanceOf(Web3.to_checksum_address(user_addr)).call()
if user_wtc > 0:
    print(f'User already has {user_wtc / 10**18:,.0f} WTC')
else:
    nonce2 = w3.eth.get_transaction_count(deployer_addr)
    tx2 = c.functions.transfer(user_addr, 50000 * 10**18).build_transaction({
        'from': deployer_addr, 'nonce': nonce2,
        'gas': 100000, 'gasPrice': w3.eth.gas_price,
        'chainId': 11155111
    })
    signed2 = deployer.sign_transaction(tx2)
    tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
    print(f'TX: {tx_hash2.hex()}')
    for i in range(30):
        time.sleep(4)
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash2)
            if receipt:
                print(f'Status: {"✅" if receipt.status == 1 else "❌"}')
                break
        except:
            pass
    else:
        print('⚠️ TX pending, check later')

# Final
time.sleep(5)
user_eth_f = w3.eth.get_balance(user_addr)
user_wtc_f = c_bal.functions.balanceOf(Web3.to_checksum_address(user_addr)).call()
print(f'\n=== Final ===')
print(f'User ETH: {w3.from_wei(user_eth_f, "ether")}')
print(f'User WTC: {user_wtc_f / 10**18:,.0f}')
if user_eth_f > 0 and user_wtc_f > 0:
    print('✅ User wallet ready for on-chain WTC transfers!')
