"""Create ben account and setup wallet"""
import sys, hashlib, base64, psycopg2, json
sys.stdout.reconfigure(encoding='utf-8')
from cryptography.fernet import Fernet

wallet = '0x18DD69502788f38d76855fbcA7f42D86b0E30329'

conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()

# Check if ben exists
cur.execute("SELECT username FROM wbankwallet WHERE username='ben'")
if cur.fetchone():
    print('ben already exists, updating wallet...')
    cur.execute("UPDATE wbankwallet SET eth_address=%s WHERE username='ben'", (wallet,))
else:
    # Create user
    import time
    cur.execute(
        "INSERT INTO wbankwallet (username, password, balance, role, sub, verify, accnumber, email, setamount, nowamount, openpay) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        ('ben', '003417', '0', 'user', 'active', 'yes', 'WB' + str(int(time.time()))[-8:], 'ben@wbank.com', 0, 0, False)
    )
    print('ben account created')

# Also set wallet address for ben
cur.execute("UPDATE wbankwallet SET eth_address=%s WHERE username='ben'", (wallet,))

conn.commit()
conn.close()

# Read deployer key from .env
_dpk = ''
with open('E:\\wbank\\.env') as _f:
    for _l in _f:
        _l = _l.strip()
        if _l.startswith('DEPLOYER_PRIVATE_KEY='):
            _dpk = _l.split('=', 1)[1].strip()
            break
if _dpk.startswith('0x'): _dpk = _dpk[2:]

from web3 import Web3 as W3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()
w3 = W3(W3.HTTPProvider('https://mainnet.base.org'))
_dep = Account.from_key(_dpk)

wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
abi = json.loads('[{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]')
c = w3.eth.contract(address=W3.to_checksum_address(wtc_addr), abi=abi)

# Check if wallet already has WTC
bal_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
c_bal = w3.eth.contract(address=W3.to_checksum_address(wtc_addr), abi=bal_abi)
existing = c_bal.functions.balanceOf(W3.to_checksum_address(wallet)).call()

if existing < 50000 * 10**18:
    nonce = w3.eth.get_transaction_count(_dep.address)
    tx = c.functions.transfer(W3.to_checksum_address(wallet), 50000 * 10**18).build_transaction({
        'from': _dep.address, 'nonce': nonce, 'gas': 100000,
        'gasPrice': w3.eth.gas_price, 'chainId': 8453
    })
    signed = _dep.sign_transaction(tx)
    h = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(h, timeout=120)
    print(f'Sent 50000 WTC: {"OK" if receipt.status == 1 else "FAIL"}')

print(f'Wallet WTC: {c_bal.functions.balanceOf(W3.to_checksum_address(wallet)).call() / 10**18}')

print(f'\n✅ ben 賬戶 ready! Send ETH to: {wallet}')
print(f'Network: Base')
