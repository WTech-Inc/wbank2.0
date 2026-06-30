import subprocess, os, time, sys
sys.stdout.reconfigure(encoding='utf-8')

print('[1] Killing old server...')
subprocess.run(['taskkill', '/f', '/im', 'python3.11.exe'], capture_output=True, timeout=10)
time.sleep(3)

print('[2] Starting server...')
bat = '''@echo off
cd /d E:\\wbank
set dataurl=postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
set HTTP_PORT=8080
set HTTPS_PORT=8443
start /B python3.11 main.py > run.log 2>&1
exit
'''
with open('E:\\wbank\\run_server.bat', 'w') as f:
    f.write(bat)

# Use start command to launch the batch file completely detached
subprocess.run('start /B "" "E:\\wbank\\run_server.bat"', shell=True, capture_output=True, timeout=5)
time.sleep(6)

print('[3] Checking...')
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python3.11.exe', '/NH'], capture_output=True, text=True, timeout=10, shell=True)
print(f'Running: {"YES" if "python3.11" in r.stdout else "NO"}')

import urllib.request
for path in ['/', '/auth/reg', '/wbank/auth/v1']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=5)
        print(f'  {path}: HTTP {r.status}')
    except urllib.error.HTTPError as e:
        print(f'  {path}: HTTP {e.code}')
    except Exception as e:
        print(f'  {path}: {e}')

log = open('E:\\wbank\\run.log', 'rb').read()
if b'Traceback' in log:
    print('\n[WARN] Errors in log:')
    print(log.decode('utf-8', 'replace')[-500:])
else:
    print(f'\n[OK] Log clear ({len(log)} bytes)')

print('\n=== DONE ===')
