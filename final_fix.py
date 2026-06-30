import subprocess, os, time, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# 1. Fix: remove ALL instances of "Route disabled" for /auth/reg
print('[1/5] Clean up old Route disabled handlers...')
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
old_len = len(m)

# Remove any route that has "/auth/reg" and "disabled"
m = re.sub(
    r"@app\.route\([\"']/auth/reg[\"'].*?\)[\s\S]*?def\s+\w+\([\s\S]*?\):[\s\S]*?(?=\n\s*@app\.route|\n\s*def\s|\Z)",
    '',
    m,
    flags=re.DOTALL
)

# Also remove any standalone disabled response
m = re.sub(r'return jsonify\(\{[\s\S]*?"Route disabled"[\s\S]*?\}\).*?\n', '', m, flags=re.DOTALL)

print(f'  Size: {old_len} -> {len(m)} ({old_len - len(m)} bytes removed)')

# Also make sure register_page is unique
count = m.count('def register_page(')
print(f'  register_page count: {count}')
if count > 1:
    # Remove all but the LAST occurrence (keep the new one from do_everything)
    parts = m.split('def register_page(')
    # Keep first part, then keep only the last occurrence
    m = parts[0] + 'def register_page(' + parts[-1]
    print(f'  Removed {count - 1} duplicate(s)')

open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

# 2. Verify syntax
print('[2/5] Verify syntax...')
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('  OK')
except py_compile.PyCompileError as e:
    print(f'  FAIL: {e}')

# 3. Kill old server
print('[3/5] Kill old server...')
subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True, timeout=10)
time.sleep(3)

# 4. Start server
print('[4/5] Start server...')
env = os.environ.copy()
env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
env['HTTP_PORT'] = '8080'
env['HTTPS_PORT'] = '8443'

# Use CREATE_NEW_CONSOLE to make it truly detached
proc = subprocess.Popen(
    ['python', 'main.py'],
    cwd='E:\\wbank',
    env=env,
    stdout=open('E:\\wbank\\run.log', 'w'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
print(f'  Started PID: {proc.pid}')
time.sleep(5)

# 5. Verify
print('[5/5] Verify...')
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
print(f'  Running: {"YES" if "python" in r.stdout else "NO"}')

import urllib.request
for path in ['/', '/auth/reg', '/wbank/auth/v1']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=5)
        body = r.read().decode('utf-8', errors='replace')[:100]
        print(f'  {path}: HTTP {r.status} - {body[:60]}...')
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')[:100]
        print(f'  {path}: HTTP {e.code} - {body[:60]}...')
    except Exception as e:
        print(f'  {path}: {e}')

print('\n=== DONE ===')
