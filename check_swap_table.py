"""Check swap_config table and test apply endpoint"""
import sys, json
sys.stdout.reconfigure(encoding="utf-8")

# Check table
import psycopg2
conn = psycopg2.connect("postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
cur = conn.cursor()
cur.execute("SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_name='swap_config')")
print(f"swap_config table: {cur.fetchone()[0]}")

cur.execute("SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_name='cashout')")
print(f"cashout table: {cur.fetchone()[0]}")

cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='swap_config' ORDER BY ordinal_position")
cols = [r[0] for r in cur.fetchall()]
print(f"swap_config columns: {cols}")

cur.execute("SELECT * FROM swap_config")
rows = cur.fetchall()
print(f"swap_config rows: {len(rows)}")
for r in rows:
    print(f"  {r}")

cur.close()
conn.close()

# Test apply via HTTP
print("\n--- Testing swap/apply ---")
import ssl, urllib.request
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# First try getting swap info
r = urllib.request.urlopen("https://127.0.0.1:9001/wbank/swap/info", context=ctx, timeout=5)
print(f"GET swap/info: {r.status} {r.read().decode()}")
