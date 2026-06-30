"""Diagnose swap/apply and audit issues"""
import sys, json, ssl, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
base = "https://127.0.0.1:9001"

# 1. Check audit_log in DB
print("=== DB Check ===")
import psycopg2
try:
    conn = psycopg2.connect("postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM audit_log")
    print(f"audit_log records: {cur.fetchone()[0]}")
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='audit_log' ORDER BY ordinal_position")
    print(f"audit_log columns: {[r[0] for r in cur.fetchall()]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"DB error: {e}")

# 2. Test admin audit API
print("\n=== Admin Audit API ===")
try:
    r = urllib.request.urlopen(f"{base}/admin/api/audit_log", context=ctx, timeout=5)
    data = json.loads(r.read())
    print(f"Status: {r.status}, Records: {len(data) if isinstance(data, list) else data}")
except Exception as e:
    print(f"Error: {e}")

# 3. Test swap/apply without auth
print("\n=== Swap Apply Test ===")
try:
    req = urllib.request.Request(f"{base}/wbank/swap/apply",
        data=json.dumps({"amount": 100}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST")
    r = urllib.request.urlopen(req, context=ctx, timeout=5)
    print(f"Status: {r.status}, Body: {r.read().decode()[:200]}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Status: {e.code}, Body: {body[:300]}")
except Exception as e:
    print(f"Error: {e}")

# 4. Check swap_config table
print("\n=== Swap Config ===")
try:
    conn = psycopg2.connect("postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
    cur = conn.cursor()
    cur.execute("SELECT * FROM swap_config")
    rows = cur.fetchall()
    print(f"Swap config: {len(rows)} rows")
    for r in rows:
        print(f"  {r}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")

# 5. Check if swap/info works (unauthenticated)
print("\n=== Swap Info ===")
try:
    r = urllib.request.urlopen(f"{base}/wbank/swap/info", context=ctx, timeout=5)
    print(f"Status: {r.status}, Body: {r.read().decode()}")
except Exception as e:
    print(f"Error: {e}")
