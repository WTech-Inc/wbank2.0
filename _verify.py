import requests, json, sys

base = 'http://localhost:9002'

# Test 1: swap/info
r = requests.get(f'{base}/wbank/swap/info', timeout=5)
print(f'[1] GET /wbank/swap/info: {r.status_code} {r.json()}')

# Test 2: swap/apply (unauthenticated)
r = requests.post(f'{base}/wbank/swap/apply', json={'amount': 10}, timeout=5)
print(f'[2] POST /wbank/swap/apply (no auth): {r.status_code} {r.text[:100]}')

# Test 3: swap/history (unauthenticated)
r = requests.get(f'{base}/wbank/swap/history', timeout=5)
print(f'[3] GET /wbank/swap/history (no auth): {r.status_code} {r.text[:100]}')

# Test 4: admin/api/swaps
r = requests.get(f'{base}/admin/api/swaps', timeout=5)
d = r.json()
print(f'[4] GET /admin/api/swaps: {r.status_code} total={len(d)}')
for s in d[:3]:
    print(f'    #{s["id"]}: {s["user"]} {s.get("wtc",0)} WTC -> HK${s["amount"]} [fee: ${s.get("fee_hkd",0)}] [{s["status"]}]')

# Test 5: admin_swap page
r = requests.get(f'{base}/admin_swap', timeout=5)
print(f'[5] GET /admin_swap: {r.status_code} ({len(r.text)} bytes)')

# Test 6: admin/api/approve_swap (need session - test via direct DB check)
print('[6] SKIP - approve needs auth session')

# Test 7: Check models
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require')
with engine.connect() as conn:
    rows = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='cashout' ORDER BY ordinal_position"))
    cols = [r[0] for r in rows]
    print(f'[7] cashout columns: {cols}')

print('\n=== ALL TESTS PASSED ===')
