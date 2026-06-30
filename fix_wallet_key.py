"""Generate new wallet with key for the user"""
import sys, hashlib, base64, psycopg2
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
from cryptography.fernet import Fernet
Account.enable_unaudited_hdwallet_features()

# Generate new wallet
acct = Account.create()
addr = Web3.to_checksum_address(acct.address)
pk = acct.key.hex()

print(f'New WBank Wallet: {addr}')
print(f'WBank has key: ✅')

# Encrypt and save to DB
secret = 'WTech2225556'
raw = hashlib.sha256(secret.encode()).digest()
fk = Fernet(base64.urlsafe_b64encode(raw))
encrypted_key = fk.encrypt(pk.encode()).decode()

conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()
cur.execute("UPDATE wbankwallet SET eth_address=%s, eth_key_encrypted=%s WHERE username='wangtry'", (addr, encrypted_key))
conn.commit()
conn.close()
print('DB updated ✅')

print(f'\nSend 0.0015 ETH to this address:')
print(f'{addr}')
print(f'Network: Base')
print(f'\n之後我可以用裡面嘅 ETH + WTC 幫你開 pool + swap')
