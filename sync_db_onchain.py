"""Sync DB balance with on-chain WTC balance"""
import sys, json, psycopg2
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))
abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address('0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'), abi=abi)
user = Web3.to_checksum_address('0xdffA9CFE9FFA749Fd93883c587193381263AA59c')
onchain = c.functions.balanceOf(user).call()
onchain_wtc = int(onchain / 10**18)
print(f'On-chain WTC: {onchain_wtc:,}')

conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()
cur.execute("SELECT balance FROM wbankwallet WHERE username='wangtry'")
db_bal = int(cur.fetchone()[0])
print(f'DB balance: {db_bal:,}')

if db_bal != onchain_wtc:
    cur.execute(f"UPDATE wbankwallet SET balance='{onchain_wtc}' WHERE username='wangtry'")
    conn.commit()
    print(f'Synced: {db_bal:,} -> {onchain_wtc:,} WTC')
else:
    print('Already in sync')
conn.close()
print('Done')
