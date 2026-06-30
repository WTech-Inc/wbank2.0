"""Transfer Sepolia ETH + WTC to user's wallet for real on-chain testing"""
import sys, json, time
sys.stdout.reconfigure(encoding='utf-8')

from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))

# Wallets
wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
user_addr = '0x53A081aeedD98D82ef29ed93818a501E2CeD2209'

# Load deployer key
pk = ''
for env_path in ['E:\\wbank\\.env', 'E:\\wbank\\contracts\\.env', 'E:\\wbank\\contracts\\deployments\\.env']:
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
    print('[ERROR] No deployer key found')
    sys.exit(1)

if pk.startswith('0x'):
    pk = pk[2:]

deployer = Account.from_key(pk)
deployer_addr = deployer.address
print(f'Deployer: {deployer_addr}')
print(f'User: {user_addr}')
print(f'WTC: {wtc_addr}\n')

# Check balances
deployer_eth = w3.eth.get_balance(deployer_addr)
user_eth = w3.eth.get_balance(user_addr)
print(f'Deployer ETH: {w3.from_wei(deployer_eth, "ether")}')
print(f'User ETH: {w3.from_wei(user_eth, "ether")}')

# 1. Send Sepolia ETH to user for gas (0.02 ETH)
if deployer_eth > 20000000000000000:
    print('\n=== Sending 0.02 SepoliaETH to user for gas ===')
    nonce = w3.eth.get_transaction_count(deployer_addr)
    tx = {
        'to': user_addr,
        'value': 20000000000000000,  # 0.02 ETH
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
        'chainId': 11155111
    }
    signed = deployer.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
    print(f'✅ Sent 0.02 SepoliaETH: {tx_hash.hex()}')
else:
    print('\n⚠️ Deployer ETH too low to send gas')

# 2. Send WTC to user (50000 WTC from deployer)
print('\n=== Sending 50000 WTC to user ===')
min_abi = json.loads('''[
    {"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},
    {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}
]''')
dec_abi = json.loads('[{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]')

wtc_contract = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=min_abi)

try:
    # Check if we need to wait for ETH to arrive
    time.sleep(2)

    nonce2 = w3.eth.get_transaction_count(deployer_addr)
    amount_wtc = 50000 * 10**18
    tx2 = wtc_contract.functions.transfer(user_addr, amount_wtc).build_transaction({
        'from': deployer_addr,
        'nonce': nonce2,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 11155111
    })
    signed2 = deployer.sign_transaction(tx2)
    tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
    receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2, timeout=120)
    if receipt2.status == 1:
        print(f'✅ Sent 50000 WTC: {tx_hash2.hex()}')
        print(f'   https://sepolia.etherscan.io/tx/{tx_hash2.hex()}')
    else:
        print('❌ WTC transfer failed')
except Exception as e:
    print(f'❌ WTC transfer error: {e}')

# Final check
print('\n=== Final Balances ===')
user_eth_final = w3.eth.get_balance(user_addr)
print(f'User ETH: {w3.from_wei(user_eth_final, "ether")} SepoliaETH')

balance_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
contract_bal = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=balance_abi)
user_wtc_final = contract_bal.functions.balanceOf(user_addr).call()
print(f'User on-chain WTC: {user_wtc_final / 10**18:,.0f} WTC')
print(f'\n✅ Now send WTC from WBank will be REAL on-chain ERC20 transfer!')
