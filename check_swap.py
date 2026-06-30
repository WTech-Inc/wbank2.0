import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
c = w3.eth.contract(address='0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB', abi=abi)

user = '0xdffA9CFE9FFA749Fd93883c587193381263AA59c'
bal = c.functions.balanceOf(Web3.to_checksum_address(user)).call()
print(f'User WTC: {bal / 10**18}')

contract = c.functions.balanceOf(Web3.to_checksum_address('0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB')).call()
print(f'WTC in contract: {contract / 10**18}')

# Send 0.0005 ETH to user as swap
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

pk = ''
with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]

deployer = Account.from_key(pk)
deployer_eth = w3.eth.get_balance(deployer.address)
print(f'Deployer ETH: {w3.from_wei(deployer_eth, "ether")}')

if deployer_eth > 500000000000000:
    tx = {
        'to': Web3.to_checksum_address(user),
        'value': w3.to_wei(0.0005, 'ether'),
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(deployer.address),
        'chainId': 8453
    }
    signed = deployer.sign_transaction(tx)
    h = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f'Sending ETH: {h.hex()}')
    receipt = w3.eth.wait_for_transaction_receipt(h, timeout=60)
    print(f'ETH sent: {receipt.status}')
else:
    print('Not enough ETH to swap')
