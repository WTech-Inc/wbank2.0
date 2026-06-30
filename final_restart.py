"""Restart - kill ALL python versions, start fresh"""
import subprocess, os, time, sys
sys.stdout.reconfigure(encoding='utf-8')

# Kill ALL python variants
print('[1/4] Killing all Python processes...')
for exe in ['python.exe', 'python3.11.exe', 'python3.exe', 'python3.9.exe', 'pythonw.exe']:
    r = subprocess.run(['taskkill', '/f', '/im', exe], capture_output=True, timeout=10)
    if r.returncode == 0:
        print(f'  Killed: {exe}')
time.sleep(3)

# Verify nothing is on port 8080
r = subprocess.run('netstat -ano | findstr ":8080"', capture_output=True, text=True, timeout=10, shell=True)
if 'LISTENING' in r.stdout:
    # Extract PID
    for line in r.stdout.split('\n'):
        if 'LISTENING' in line:
            parts = line.strip().split()
            pid = parts[-1]
            print(f'  Port 8080 still in use by PID {pid}, killing...')
            subprocess.run(['taskkill', '/f', '/pid', pid], capture_output=True, timeout=10)
    time.sleep(2)
else:
    print('  Port 8080 is free')

# Verify routes in main.py
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
print(f'\n[2/4] Route check:')
print(f'  /auth/reg: {"YES" if "/auth/reg" in m else "NO"}')
print(f'  register_page: {"YES" if "def register_page" in m else "NO"}')
print(f'  File size: {len(m)} bytes')

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('  Syntax: OK')
except py_compile.PyCompileError as e:
    print(f'  Syntax: FAIL - {e}')

# Check wbank_web3.py
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
print(f'  ERC20 transfer: {"YES" if "ERC20 WTC Transfer" in w3 else "NO (check if original)"}')

# Start using python3.11.exe (same as the old server)
print(f'\n[3/4] Starting server with python3.11.exe...')
env = os.environ.copy()
env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
env['HTTP_PORT'] = '8080'
env['HTTPS_PORT'] = '8443'

python_path = r'C:\Users\wangtry\AppData\Local\Microsoft\WindowsApps\python3.11.exe'
if not os.path.exists(python_path):
    python_path = 'python3.11.exe'
    print(f'  Using: {python_path} (PATH)')
else:
    print(f'  Using: {python_path}')

proc = subprocess.Popen(
    [python_path, 'main.py'],
    cwd='E:\\wbank',
    env=env,
    stdout=open('E:\\wbank\\run.log', 'w'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
print(f'  Started PID: {proc.pid}')
time.sleep(5)

# Verify
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python3.11.exe', '/NH'], capture_output=True, text=True, timeout=10)
print(f'  Running: {"YES" if "python3.11" in r.stdout else "NO"}')

# Test
print(f'\n[4/4] Testing routes...')
import urllib.request
for path in ['/', '/auth/reg', '/wbank/auth/v1']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=5)
        body = r.read().decode('utf-8', errors='replace')[:100]
        print(f'  {path}: HTTP {r.status} OK')
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')[:100]
        print(f'  {path}: HTTP {e.code}')
        if 'register' in body.lower() or 'regist' in body.lower() or 'WBank' in body:
            print(f'    Content contains registration page!')
    except Exception as e:
        print(f'  {path}: {e}')

# Check for errors
log = open('E:\\wbank\\run.log', 'rb').read()
errors = log.count(b'Traceback')
print(f'\nLog errors: {errors}')
if errors > 0:
    # Print the last error
    log_text = log.decode('utf-8', 'replace')
    idx = log_text.rfind('Traceback')
    if idx >= 0:
        print(log_text[idx:idx+500])

print('\n=== Done ===')
