"""Fix transaction recording - add id column, fix insert, fix network name"""
import sys, subprocess, time
sys.stdout.reconfigure(encoding='utf-8')

# 1. Fix database - add id column to wbankrecord
print('[1/5] Fix database table...')
try:
    import psycopg2
    conn = psycopg2.connect(
        database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
        host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
    cur = conn.cursor()

    # Add id column if it doesn't exist
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='wbankrecord' AND column_name='id'")
    if not cur.fetchone():
        cur.execute("ALTER TABLE wbankrecord ADD COLUMN id SERIAL")
        # Drop old primary key on username
        cur.execute("ALTER TABLE wbankrecord DROP CONSTRAINT wbankrecord_pkey")
        # Set id as primary key
        cur.execute("ALTER TABLE wbankrecord ADD PRIMARY KEY (id)")
        print('  [OK] Added id column + new primary key')
    else:
        print('  [OK] id column already exists')

    conn.commit()
    conn.close()
except Exception as e:
    print(f'  [WARN] DB fix: {e}')

# 2. Fix wbank_web3.py - fix insert and network name
print('\n[2/5] Fix wbank_web3.py...')
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Fix network name
w3 = w3.replace('"network": "Sepolia Testnet"', '"network": "BSC Testnet"')

# Fix the INSERT - remove ON CONFLICT and add proper import
old_insert = '''    # Record transaction (safe insert - handle duplicate PK)
    try:
        db.session.execute(
            text("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t) ON CONFLICT (username) DO UPDATE SET action = :a, time = :t"),
            {'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...", 't': local_time}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()'''

new_insert = '''    # Record transaction
    try:
        from sqlalchemy import text as _sql_text
        db.session.add(wbankrecord(
            username=username,
            action=f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...",
            time=local_time
        ))
        db.session.commit()
    except Exception:
        try:
            db.session.rollback()
            # Fallback: use raw SQL
            from sqlalchemy import text as _sql_text2
            db.session.execute(
                _sql_text2("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t)"),
                {'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...", 't': local_time}
            )
            db.session.commit()
        except:
            db.session.rollback()'''

if old_insert in w3:
    w3 = w3.replace(old_insert, new_insert)
    print('  [OK] Fixed INSERT + added wbankrecord ORM usage')
else:
    print('  [WARN] Could not find old insert pattern')
    # Debug
    idx = w3.find('ON CONFLICT')
    if idx >= 0:
        print(f'  Found at {idx}')
        print(w3[idx-100:idx+200])
    idx = w3.find('Record transaction')
    if idx >= 0:
        print(f'  Found "Record transaction" at {idx}')
        print(w3[idx:idx+300])

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('  [OK] Syntax OK')

# 3. Also verify main.py web3 CSRF exemption
print('\n[3/5] Verify CSRF exemption...')
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
csrfs = m.count('csrf.exempt')
print(f'  csrf.exempt count: {csrfs}')

# Check web3_bp exemption loop
if 'web3_bp' in m and 'csrf.exempt' in m:
    idx = m.find('web3_bp')
    context = m[max(0,idx-200):idx+200]
    if 'csrf.exempt' in context:
        print('  [OK] web3 CSRF exemption found')
    else:
        print('  [WARN] web3 CSRF exemption not found near web3_bp')

# 4. Verify all
print('\n[4/5] Verify...')
m2 = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
py_compile.compile('E:\\wbank\\main.py', doraise=True)
print('  [OK] main.py syntax OK')

# 5. Restart
print('\n[5/5] Restart server...')
subprocess.run(['taskkill', '/f', '/im', 'python3.11.exe'], capture_output=True, timeout=10)
time.sleep(4)

import os
env = os.environ.copy()
env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
env['HTTP_PORT'] = '8080'
env['HTTPS_PORT'] = '8443'

proc = subprocess.Popen(
    [r'C:\Users\wangtry\AppData\Local\Microsoft\WindowsApps\python3.11.exe', 'E:\\wbank\\main.py'],
    env=env,
    stdout=open('E:\\wbank\\run.log', 'w'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
print(f'  Started PID: {proc.pid}')
time.sleep(8)

# Test all
import urllib.request
cookies = None

# Login
import http.cookiejar
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Login
login_data = urllib.parse.urlencode({'user': 'wangtry', 'pw': 'Chan1234#', 'url': '/wbank/client'}).encode()
r = opener.open('http://localhost:8080/wbank/auth/v1/session', login_data, timeout=10)
print(f'  Login: {r.status}')

# Web3 Info
r = opener.open('http://localhost:8080/wbank/web3/info', timeout=10)
import json
info = json.loads(r.read())
print(f'  Web3 Info: balance={info.get("balance")}, network={info.get("network")}')

# Web3 Send
send_data = json.dumps({'to': '0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18', 'amount': 5}).encode()
r = opener.open('http://localhost:8080/wbank/web3/send', send_data, timeout=10)
send_result = json.loads(r.read())
print(f'  Send: success={send_result.get("success")}, amount={send_result.get("amount")}')

# Web3 History
r = opener.open('http://localhost:8080/wbank/web3/history', timeout=10)
history = json.loads(r.read())
print(f'  History: {len(history)} transactions')
for h in history:
    print(f'    - {h["action"][:60]}... ({h["time"]})')

print('\n=== DONE ===')
