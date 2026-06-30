"""Send remaining deployer ETH to user"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))

pk = ''
with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]

deployer = Account.from_key(pk)
user = '0xdffA9CFE9FFA749Fd93883c587193381263AA59c'

eth_bal = w3.eth.get_balance(deployer.address)
gas = w3.to_wei(0.0001, 'ether')
send_amt = eth_bal - gas

print(f'Deployer ETH: {w3.from_wei(eth_bal, "ether")}')
print(f'Sending: {w3.from_wei(send_amt, "ether")} ETH')

if send_amt > 0:
    nonce = w3.eth.get_transaction_count(deployer.address)
    tx = {
        'to': Web3.to_checksum_address(user),
        'value': send_amt,
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
        'chainId': 8453
    }
    signed = deployer.sign_transaction(tx)
    h = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f'TX: {h.hex()}')
    r = w3.eth.wait_for_transaction_receipt(h, timeout=60)
    print(f'Status: {"OK" if r.status == 1 else "FAIL"}')
else:
    print('Deployer has no ETH left to send')
