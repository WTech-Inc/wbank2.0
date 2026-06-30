"""Generate and save deployer wallet"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

acct = Account.create()
addr = Web3.to_checksum_address(acct.address)

print(f'Address: {addr}')
print(f'Valid: {Web3.is_address(addr)}')
print(f'Checksum: {addr}')
print(f'Private Key: 0x{acct.key.hex()}')

# Save
with open('E:\\wbank\\.env', 'w') as f:
    f.write(f'DEPLOYER_PRIVATE_KEY=0x{acct.key.hex()}\n')
print(f'\nSaved to E:\\\\wbank\\\\.env')
print(f'\nSend Sepolia ETH to: {addr}')
