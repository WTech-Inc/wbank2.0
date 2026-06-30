"""Test if WTC is working end-to-end"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))

# Contract addresses
wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
user_addr = '0x53A081aeedD98D82ef29ed93818a501E2CeD2209'
deployer_addr = '0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7'

print('=== WTC Token Status ===')
print(f'Contract: {wtc_addr}')
print(f'User wallet: {user_addr}')
print(f'Deployer: {deployer_addr}')
print(f'Sepolia connected: {w3.is_connected()}\n')

# Check ETH balances
print(f'User ETH: {w3.from_wei(w3.eth.get_balance(user_addr), "ether")} SepoliaETH')
print(f'Deployer ETH: {w3.from_wei(w3.eth.get_balance(deployer_addr), "ether")} SepoliaETH')

# Check WTC balance
min_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"}]')
contract = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=min_abi)

try:
    total = contract.functions.totalSupply().call()
    print(f'\nWTC Total Supply: {total / 10**18:,.0f} WTC')
except Exception as e:
    print(f'Total supply error: {e}')

try:
    deployer_wtc = contract.functions.balanceOf(Web3.to_checksum_address(deployer_addr)).call()
    print(f'Deployer WTC: {deployer_wtc / 10**18:,.0f} WTC')
except Exception as e:
    print(f'Deployer WTC error: {e}')

try:
    user_wtc = contract.functions.balanceOf(Web3.to_checksum_address(user_addr)).call()
    print(f'User on-chain WTC: {user_wtc / 10**18:,.0f} WTC')
except Exception as e:
    print(f'User WTC error: {e}')

# Check DB balance
print('\n=== DB Balance (what user sees in WBank) ===')
import psycopg2
conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()
cur.execute("SELECT username, balance FROM wbankwallet")
for r in cur.fetchall():
    print(f'{r[0]}: {r[1]} WTC (DB)')
cur.execute("SELECT username, action, time FROM wbankrecord ORDER BY id DESC LIMIT 3")
for r in cur.fetchall():
    print(f'  TX: {r[1][:60]}... ({r[2]})')
conn.close()

print('\n=== Verdict ===')
if user_wtc > 0:
    print('✅ User has on-chain WTC tokens!')
else:
    print('⚠️ User has 0 on-chain WTC (all WTC is database-only for now)')
    print('   Initial 10M WTC was minted to deployer wallet')
    print('   Need to transfer some to user wallet or deposit function')

print(f'\nSend Sepolia ETH to user wallet for gas:')
print(f'{user_addr}')
