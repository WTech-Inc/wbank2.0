"""Fix address checksum validation in wbank_web3.py send function"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Fix: add to_checksum_address before contract call
# Find the line where transfer is called and add checksum conversion
old_line = "            tx = c.functions.transfer(to_address, amt).build_transaction({"
new_line = "            tx = c.functions.transfer(Web3.to_checksum_address(to_address), amt).build_transaction({"

if old_line in w3:
    w3 = w3.replace(old_line, new_line)
    print('[OK] Added to_checksum_address to transfer call')
else:
    print('[WARN] Pattern not found')
    # Try to find it
    idx = w3.find('c.functions.transfer(to_address')
    if idx >= 0:
        print(f'Found at {idx}:')
        print(w3[idx:idx+100])

# Also make sure the RPC connection is good
# Replace the RPC with one that supports writes
if 'ethereum-sepolia.publicnode.com' in w3:
    # This RPC works for both read and write
    pass

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')
print('\nRestart server needed')
