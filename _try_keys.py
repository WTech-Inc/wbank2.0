"""Try different SECRET_KEY combinations"""
import hashlib, base64
from cryptography.fernet import Fernet, InvalidToken
import psycopg2

# Get encrypted key
c = psycopg2.connect(host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', dbname='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz', sslmode='require')
cur = c.cursor()
cur.execute("SELECT eth_key_encrypted FROM wbankwallet WHERE username='wangtry'")
ek = cur.fetchone()[0]
c.close()
print(f'Encrypted key: {ek[:50]}...')

# Try different SECRET_KEY values
secrets = [
    hashlib.sha256("WTech2225556".encode()).hexdigest(),  # current
    "WTech2225556",  # maybe raw string
    hashlib.sha256("wbank".encode()).hexdigest(),
    "wbank",
    hashlib.md5("WTech2225556".encode()).hexdigest(),
    "WTech2225556!",
]

for i, secret in enumerate(secrets):
    try:
        raw = hashlib.sha256(str(secret).encode()).digest()
        b64 = base64.urlsafe_b64encode(raw)
        k = Fernet(b64)
        pk = k.decrypt(ek.encode(), ttl=None).decode()
        print(f'KEY #{i} WORKS! secret={str(secret)[:30]}')
        print(f'  Private key: {pk[:40]}...')
        break
    except InvalidToken:
        print(f'Key #{i}: wrong ({str(secret)[:30]}...)')
    except Exception as e:
        print(f'Key #{i}: error {e}')
