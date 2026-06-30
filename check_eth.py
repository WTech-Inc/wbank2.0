import sys
sys.stdout.reconfigure(encoding='utf-8')

from web3 import Web3
import psycopg2

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))

# Check user's existing wallet
addr = '0x53A081aeedD98D82ef29ed93818a501E2CeD2209'
bal = w3.eth.get_balance(addr)
print(f'User wallet ({addr}): {w3.from_wei(bal, "ether")} ETH')

# Check DB wallets
conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()
cur.execute("SELECT username, eth_address FROM wbankwallet WHERE eth_address IS NOT NULL")
for r in cur.fetchall():
    addr2 = r[1]
    try:
        bal2 = w3.eth.get_balance(addr2)
        print(f'{r[0]} wallet ({addr2}): {w3.from_wei(bal2, "ether")} Sepolia ETH')
    except:
        print(f'{r[0]} wallet ({addr2}): error checking')
conn.close()

# Check deployer wallet
deployer = '0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7'
bal3 = w3.eth.get_balance(deployer)
print(f'Deployer ({deployer}): {w3.from_wei(bal3, "ether")} Sepolia ETH')
