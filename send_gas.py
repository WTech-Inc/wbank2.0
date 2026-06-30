"""Send Sepolia ETH to user's wallet + check tx history HTML"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com', request_kwargs={'timeout': 60}))

# Load deployer key
pk = ''
with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]
deployer = Account.from_key(pk)

# User's new wallet
user = '0xdffA9CFE9FFA749Fd93883c587193381263AA59c'
user_ws = Web3.to_checksum_address(user)
user_eth = w3.eth.get_balance(user_ws)
print(f'User ETH before: {w3.from_wei(user_eth, "ether")}')

# Send 0.02 SepoliaETH for gas
if user_eth < 20000000000000000:
    nonce = w3.eth.get_transaction_count(deployer.address)
    tx = {
        'to': user_ws,
        'value': w3.to_wei(0.02, 'ether'),
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
        'chainId': 11155111
    }
    signed = deployer.sign_transaction(tx)
    h = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f'ETH TX: {h.hex()}')
    receipt = w3.eth.wait_for_transaction_receipt(h, timeout=120)
    print(f'Status: {"OK" if receipt.status == 1 else "FAIL"}')

print(f'User ETH after: {w3.from_wei(w3.eth.get_balance(user_ws), "ether")}')

# Also send some on-chain WTC
wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
import json
abi = json.loads('[{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=abi)
bal_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
c_bal = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=bal_abi)
user_wtc = c_bal.functions.balanceOf(user_ws).call()
print(f'User on-chain WTC before: {user_wtc / 10**18}')

if user_wtc == 0:
    nonce2 = w3.eth.get_transaction_count(deployer.address)
    tx2 = c.functions.transfer(user_ws, 50000 * 10**18).build_transaction({
        'from': deployer.address, 'nonce': nonce2,
        'gas': 100000, 'gasPrice': w3.eth.gas_price,
        'chainId': 11155111
    })
    signed2 = deployer.sign_transaction(tx2)
    h2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
    print(f'WTC TX: {h2.hex()}')
    receipt2 = w3.eth.wait_for_transaction_receipt(h2, timeout=120)
    print(f'Status: {"OK" if receipt2.status == 1 else "FAIL"}')

print(f'User WTC after: {c_bal.functions.balanceOf(user_ws).call() / 10**18}')
print('\nDone')
