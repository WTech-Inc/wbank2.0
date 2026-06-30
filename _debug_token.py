"""Debug Fernet token structure"""
import hashlib, base64, psycopg2
from cryptography.fernet import Fernet

# Our key
app_secret = hashlib.sha256("WTech2225556".encode()).hexdigest()
raw = hashlib.sha256(app_secret.encode()).digest()
b64 = base64.urlsafe_b64encode(raw)
k = Fernet(b64)
print(f'Our key: {b64}')

# Get encrypted key from DB
c = psycopg2.connect(host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', dbname='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz', sslmode='require')
cur = c.cursor()
cur.execute("SELECT username, eth_key_encrypted FROM wbankwallet WHERE username='wangtry'")
r = cur.fetchone()
c.close()

username, ek = r
print(f'\nUser: {username}')
print(f'Encrypted token: {ek}')
print(f'Token length: {len(ek)}')

# Check if there are other users with different keys
c2 = psycopg2.connect(host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', dbname='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz', sslmode='require')
cur2 = c2.cursor()
cur2.execute("SELECT username FROM wbankwallet WHERE eth_key_encrypted IS NOT NULL AND eth_key_encrypted != ''")
users = cur2.fetchall()
c2.close()
print(f'\nTotal users with encrypted keys: {len(users)}')
for u in users[:3]:
    print(f'  - {u[0]}')

# Try to decrypt by extracting version byte
import re
parts = ek.split('.')
print(f'\nToken parts: {len(parts)}')
for i, p in enumerate(parts):
    print(f'  Part {i}: len={len(p)}, starts={p[:10]}...')

# Fernet v2 token format: version(1) + timestamp(8) + IV(16) + ciphertext + HMAC(32)
try:
    # Add padding for base64 decode of the full token
    padded = ek + '=' * (4 - len(ek) % 4) if len(ek) % 4 else ek
    decoded = base64.urlsafe_b64decode(padded)
    print(f'\nDecoded token ({len(decoded)} bytes):')
    print(f'  Version: {decoded[0]}')
    print(f'  Timestamp: {int.from_bytes(decoded[1:9], "big")}')
    print(f'  IV: {decoded[9:25].hex()}')
    print(f'  Ciphertext: {decoded[25:-32].hex()[:40]}...')
    print(f'  HMAC: {decoded[-32:].hex()[:40]}...')
except Exception as e:
    print(f'Cannot decode: {e}')
