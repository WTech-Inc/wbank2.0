"""Check WTC transaction records"""
import sys, json
sys.stdout.reconfigure(encoding="utf-8")

import psycopg2
conn = psycopg2.connect("postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
cur = conn.cursor()
cur.execute("SELECT username, action, time FROM wbankrecord WHERE action LIKE '%WTC%' ORDER BY time DESC LIMIT 10")
rows = cur.fetchall()
if not rows:
    print("No WTC records found")
else:
    for r in rows:
        print(f"[{r[2]}] {r[0]}: {r[1][:150]}")
cur.close()
conn.close()

from web3 import Web3
w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))
dep = "0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7"
wtc_addr = "0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB"
min_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=min_abi)
bal = c.functions.balanceOf(dep).call()
print(f"\nDeployer WTC: {bal / 10**18} WTC")
eth_bal = w3.eth.get_balance(dep)
print(f"Deployer ETH: {w3.from_wei(eth_bal, 'ether')} ETH")
print(f"Connected: {w3.is_connected()}")
