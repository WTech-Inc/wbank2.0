import sys, hashlib, base64, traceback
from cryptography.fernet import Fernet, InvalidToken

secret = hashlib.sha256("WTech2225556".encode()).hexdigest()
raw = hashlib.sha256(secret.encode()).digest()
b64_key = base64.urlsafe_b64encode(raw)
k = Fernet(b64_key)
print(f'Fernet key len: {len(b64_key)}')

import psycopg2
c = psycopg2.connect(host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', dbname='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz', sslmode='require')
cur = c.cursor()
cur.execute("SELECT eth_key_encrypted FROM wbankwallet WHERE username='wangtry'")
ek = cur.fetchone()[0]
c.close()
print(f'Encrypted: type={type(ek).__name__}, len={len(str(ek))}')

try:
    pk = k.decrypt(ek.encode() if isinstance(ek, str) else ek)
    pk = pk.decode()
    print(f'OK: {pk[:40]}...')
except InvalidToken as e:
    print(f'InvalidToken: {e}')
    with open('_dec_error.txt', 'w') as ef:
        ef.write(f'InvalidToken: {e}\n{traceback.format_exc()}')
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
    with open('_dec_error.txt', 'w') as ef:
        ef.write(f'{type(e).__name__}: {e}\n{traceback.format_exc()}')
