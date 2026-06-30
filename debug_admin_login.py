"""Debug admin login"""
import sys, ssl, urllib.request, urllib.parse, json
sys.stdout.reconfigure(encoding="utf-8")

# Check exact DB values
import psycopg2
conn = psycopg2.connect("postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
cur = conn.cursor()
cur.execute("SELECT username, password, role, length(password) FROM wbankwallet WHERE username='wbank'")
r = cur.fetchone()
print(f"DB: user={repr(r[0])}, pw={repr(r[1])}, role={repr(r[2])}, pw_len={r[3]}")
print(f"pw == 'wbank@2026': {r[1] == 'wbank@2026'}")
print(f"role == 'admin': {r[2] == 'admin'}")
cur.close()
conn.close()

# Now test via HTTP
print("\n--- Testing HTTP login ---")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

data = urllib.parse.urlencode({"user": "wbank", "pw": "wbank@2026"}).encode()
req = urllib.request.Request("https://127.0.0.1:9001/admin/login", data=data, method="POST")
r = urllib.request.urlopen(req, context=ctx, timeout=5)
print(f"Login: {r.status}")
print(f"URL: {r.url}")
print(f"Headers: {dict(r.headers)}")
body = r.read().decode("utf-8", "replace")[:500]
print(f"Body: {body[:300]}")
