"""Test direct on-chain ERC20 transfer to find the error"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

# Use the user's wallet
# We need the private key - it's stored encrypted in DB
# Let's use the deployer wallet instead which we know works
pk = ''
with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com', request_kwargs={'timeout': 30}))
print(f'Connected: {w3.is_connected()}')

deployer = Account.from_key(pk)
print(f'Deployer: {deployer.address}')
print(f'Deployer nonce: {w3.eth.get_transaction_count(deployer.address)}')
print(f'Deployer ETH: {w3.from_wei(w3.eth.get_balance(deployer.address), "ether")}')
print(f'Gas price: {w3.from_wei(w3.eth.gas_price, "gwei")} Gwei')

# Transfer 1 WTC directly
wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
abi = json.loads('[{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=abi)

try:
    to_addr = '0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18'
    nonce = w3.eth.get_transaction_count(deployer.address)
    print(f'\nBuilding tx (nonce: {nonce})...')
    tx = c.functions.transfer(to_addr, 1 * 10**18).build_transaction({
        'from': deployer.address,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 11155111
    })
    print(f'Built OK, signing...')
    signed = deployer.sign_transaction(tx)
    print(f'Signed, sending...')
    raw = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f'Sent! TX: {raw.hex()}')
    print(f'Waiting for receipt...')
    receipt = w3.eth.wait_for_transaction_receipt(raw, timeout=120)
    print(f'Status: {"✅" if receipt.status == 1 else "❌"}')
    print(f'Gas used: {receipt.gasUsed}')
    print(f'https://sepolia.etherscan.io/tx/{raw.hex()}')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
