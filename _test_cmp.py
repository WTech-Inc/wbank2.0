"""Compare Fernet key generation methods"""
import hashlib, base64

# Method 1: Same as get_encryption_key
app_secret = hashlib.sha256("WTech2225556".encode()).hexdigest()
print(f'SECRET_KEY: {app_secret}')
raw = hashlib.sha256(app_secret.encode()).digest()
b64 = base64.urlsafe_b64encode(raw)
print(f'Method 1 Fernet key: {b64}')

# Method 2: Direct
app_secret2 = hashlib.sha256("WTech2225556".encode()).hexdigest()
raw2 = hashlib.sha256(app_secret2.encode()).digest()
b642 = base64.urlsafe_b64encode(raw2)
print(f'Method 2 Fernet key: {b642}')
print(f'Match: {b64 == b642}')

# Read the encrypted key
import psycopg2
c = psycopg2.connect(host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', dbname='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz', sslmode='require')
cur = c.cursor()
cur.execute("SELECT eth_key_encrypted FROM wbankwallet WHERE username='wangtry'")
ek = cur.fetchone()[0]
c.close()
print(f'\nStored encrypted key: {ek[:40]}...')

# Try to decrypt
from cryptography.fernet import Fernet
k = Fernet(b64)
try:
    pk = k.decrypt(ek.encode()).decode()
    print(f'DECRYPTED: {pk[:40]}...')
except Exception as e:
    print(f'Cannot decrypt: {e}')
