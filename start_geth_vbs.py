"""Start Geth dev node via VBS script"""
import sys, os, subprocess, time
sys.stdout.reconfigure(encoding='utf-8')

# Write VBS script
vbs = '''Dim WshShell
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "E:\\wbank\\private-chain"
WshShell.Run "E:\\wbank\\private-chain\\geth.exe --dev --http --http.addr 0.0.0.0 --http.port 8545 --http.api eth,web3,net,personal --http.corsdomain * --http.vhosts * --nodiscover --ipcdisable --dev.gaslimit 9999999999", 0, False
'''

vbs_path = 'E:\\wbank\\private-chain\\start_geth.vbs'
with open(vbs_path, 'w') as f:
    f.write(vbs)

print('[OK] VBS script created')

# Kill old
subprocess.run(['taskkill', '/f', '/im', 'geth.exe'], capture_output=True, timeout=10)
time.sleep(2)

# Start via VBS
subprocess.run(['cscript', '//nologo', vbs_path], capture_output=True, timeout=10)
time.sleep(5)

# Check
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq geth.exe', '/NH'], capture_output=True, text=True, timeout=10, shell=True)
print(f'Running: {"YES" if "geth" in r.stdout else "NO"}')

# Test RPC
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
print(f'Connected: {w3.is_connected()}')
if w3.is_connected():
    print(f'Block: {w3.eth.block_number}')

# Write start_chain.bat for user to double-click
bat = '''@echo off
cd /d E:\\wbank\\private-chain
echo Starting WTC Private Chain...
echo RPC: http://localhost:8545
echo ChainID: 456789 (dev mode)
echo.
start /B geth.exe --dev --http --http.addr 0.0.0.0 --http.port 8545 --http.api eth,web3,net,personal --http.corsdomain * --http.vhosts * --nodiscover --ipcdisable --dev.gaslimit 9999999999
echo Started!
echo MetaMask: http://localhost:8545 | ChainID: 456789
pause
'''
with open('E:\\wbank\\private-chain\\start_chain.bat', 'w') as f:
    f.write(bat)

print('\nDone!')
print('Geth dev node started on http://localhost:8545')
print('ChainID: 456789')
print('MetaMask: RPC http://223.18.36.147:8545 | ChainID: 456789')
