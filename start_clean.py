"""Simple clean start"""
import subprocess, os, time, sys
sys.stdout.reconfigure(encoding='utf-8')

# Check routes
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
print('/auth/reg in main.py:', '/auth/reg' in m)
print('def register_page:', 'def register_page' in m)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax: OK')
except py_compile.PyCompileError as e:
    print(f'Syntax: {e}')
    sys.exit(1)

# Start server
env = os.environ.copy()
env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
env['HTTP_PORT'] = '8080'
env['HTTPS_PORT'] = '8443'

python_exe = sys.executable  # Use same Python as the script running on
proc = subprocess.Popen(
    [python_exe, 'main.py'],
    cwd='E:\\wbank',
    env=env,
    stdout=open('E:\\wbank\\run.log', 'w'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
print(f'Started PID: {proc.pid}')
time.sleep(5)

# Verify
r = subprocess.run('tasklist /FI "PID eq ' + str(proc.pid) + '" /NH', capture_output=True, text=True, timeout=10, shell=True)
print(f'Running: {"YES" if str(proc.pid) in r.stdout else "NO"}')

# Test
import urllib.request
for path in ['/', '/auth/reg', '/wbank/auth/v1']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=5)
        print(f'{path}: HTTP {r.status}')
    except urllib.error.HTTPError as e:
        print(f'{path}: HTTP {e.code}')
    except Exception as e:
        print(f'{path}: {e}')

# Log
log = open('E:\\wbank\\run.log', 'rb').read()
errs = log.count(b'Traceback')
if errs:
    print(f'\nErrors: {errs}')
    print(log.decode('utf-8','replace')[-500:])
else:
    print(f'\nLog OK ({len(log)} bytes)')

print('\n=== Done ===')
