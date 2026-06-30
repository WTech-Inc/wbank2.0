import requests, json, sys

base = 'http://localhost:9002'

def test(name, method, path, **kwargs):
    url = f'{base}{path}'
    try:
        if method == 'GET':
            r = requests.get(url, timeout=10, **kwargs)
        else:
            r = requests.post(url, timeout=10, **kwargs)
        print(f'[{name}] {method} {path}: {r.status_code}')
        try:
            j = r.json()
            print(f'  JSON: {json.dumps(j, ensure_ascii=False)[:200]}')
        except:
            print(f'  Text: {r.text[:200]}')
        return r
    except Exception as e:
        print(f'[{name}] ERROR: {e}')
        return None

# Test 1: swap/info
test(1, 'GET', '/wbank/swap/info')

# Test 2: swap/apply (unauthenticated)
test(2, 'POST', '/wbank/swap/apply', json={'amount': 10})

# Test 3: swap/history (unauthenticated)
test(3, 'GET', '/wbank/swap/history')

# Test 4: admin swap page
test(4, 'GET', '/admin_swap')

# Test 5: admin api
test(5, 'GET', '/admin/api/swap_rate')

# Test 6: admin api swaps
test(6, 'GET', '/admin/api/swaps')

# Test 7: Check DB columns
print()
print('[7] Checking DB columns...')
try:
    from sqlalchemy import create_engine, text
    engine = create_engine('postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require')
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='cashout' ORDER BY ordinal_position"))
        cols = [r[0] for r in rows]
        print(f'  cashout columns: {cols}')
except Exception as e:
    print(f'  DB error: {e}')

print()
print('=== DONE ===')
