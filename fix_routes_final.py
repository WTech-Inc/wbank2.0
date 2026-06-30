"""Fix: add /auth/ to allowed routes in before_request"""
import sys, subprocess, os, time
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Add /auth/ to the allowed prefixes /wbank/ check
old = "if path == '/' or path == '/wbank' or path.startswith('/wbank/'):"
new = "if path == '/' or path == '/wbank' or path.startswith('/wbank/') or path == '/auth/reg' or path.startswith('/auth/'):"

if old in m:
    m = m.replace(old, new)
    print('[OK] /auth/ added to allowed routes')
else:
    print('[WARN] Pattern not found')
    # Try alternative
    for i, line in enumerate(m.split('\n')):
        if 'path.startswith' in line and '/wbank/' in line:
            print(f'  Found at line {i+1}: {line.strip()[:100]}')

open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('[OK] Syntax OK')
except py_compile.PyCompileError as e:
    print(f'[FAIL] {e}')

# Kill and restart
print('[RESTART] Killing server...')
subprocess.run(['taskkill', '/f', '/im', 'python3.11.exe'], capture_output=True, timeout=10)
subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True, timeout=10)
time.sleep(3)

print('[RESTART] Starting server...')
env = os.environ.copy()
env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
env['HTTP_PORT'] = '8080'
env['HTTPS_PORT'] = '8443'

python_exe = r'C:\Users\wangtry\AppData\Local\Microsoft\WindowsApps\python3.11.exe'
proc = subprocess.Popen(
    [python_exe, 'E:\\wbank\\main.py'],
    env=env,
    stdout=open('E:\\wbank\\run.log', 'w'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
print(f'[RESTART] PID: {proc.pid}')
time.sleep(5)

# Verify
r = subprocess.run('tasklist /FI "PID eq ' + str(proc.pid) + '" /NH', capture_output=True, text=True, timeout=10, shell=True)
print(f'[CHECK] Running: {"YES" if str(proc.pid) in r.stdout else "NO"}')

# Test routes
import urllib.request
for path in ['/', '/auth/reg', '/wbank/auth/v1']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=5)
        body = r.read().decode('utf-8', errors='replace')[:80]
        print(f'  {path}: HTTP {r.status} {"OK" if r.status == 200 else ""}')
        if r.status == 200 and 'register' in body.lower():
            print(f'    -> Contains registration page!')
    except urllib.error.HTTPError as e:
        print(f'  {path}: HTTP {e.code}')
    except Exception as e:
        print(f'  {path}: {e}')

# Check log
log = open('E:\\wbank\\run.log', 'rb').read()
if b'Traceback' in log:
    print(f'\n[ERROR] Traceback in log!')
    err = log.decode('utf-8', 'replace')
    idx = err.rfind('Traceback')
    print(err[idx:idx+500])
else:
    print(f'\n[OK] Log clear ({len(log)} bytes)')

print('\n=== DONE ===')
