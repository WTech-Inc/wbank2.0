"""Test decrypting private key with actual Flask app context"""
import sys, hashlib, base64
from cryptography.fernet import Fernet

# Replicate get_encryption_key logic
secret = hashlib.sha256("WTech2225556".encode()).hexdigest()
raw = hashlib.sha256(secret.encode()).digest()
b64_key = base64.urlsafe_b64encode(raw)
k = Fernet(b64_key)
print(f'Fernet key: {b64_key[:20]}...')

# Get encrypted key from DB
import psycopg2
c = psycopg2.connect(host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', dbname='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz', sslmode='require')
cur = c.cursor()
cur.execute("SELECT eth_key_encrypted FROM wbankwallet WHERE username='wangtry'")
ek = cur.fetchone()[0]
print(f'Encrypted key len: {len(ek)}')
c.close()

try:
    pk = k.decrypt(ek.encode()).decode()
    print(f'Decrypted PK: {pk[:20]}...')
    print('SUCCESS: Private key decrypts correctly')
except Exception as e:
    print(f'DECRYPT FAILED: {e}')
