"""Start server using a batch file approach (works via SSH)"""
import subprocess, os, time, sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Kill old
subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True, timeout=10)
time.sleep(2)
print('[1] Old processes killed')

# 2. Create batch file
bat = '''@echo off
cd /d E:\\wbank
set dataurl=postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
set HTTP_PORT=8080
set HTTPS_PORT=8443
python main.py > run.log 2>&1
'''

with open('E:\\wbank\\start.bat', 'w') as f:
    f.write(bat)
print('[2] Batch file created')

# 3. Start via scheduled task (most reliable for remote detached process)
subprocess.run([
    'schtasks', '/create', '/tn', 'WBankServer', '/tr',
    'E:\\wbank\\start.bat', '/sc', 'once', '/st', '00:00',
    '/f', '/IT', '/RL', 'HIGHEST'
], capture_output=True, text=True, timeout=15)

# Run the task immediately
subprocess.run(['schtasks', '/run', '/tn', 'WBankServer'], capture_output=True, timeout=15)

time.sleep(5)

# Delete the task
subprocess.run(['schtasks', '/delete', '/tn', 'WBankServer', '/f'], capture_output=True, timeout=10)

time.sleep(3)

# Check
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
running = 'python' in r.stdout
print(f'[3] Running: {"YES" if running else "NO"}')

# Test
import urllib.request
for path in ['/', '/auth/reg', '/wbank/auth/v1']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=5)
        body = r.read().decode('utf-8', errors='replace')[:80]
        print(f'  {path}: HTTP {r.status}')
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')[:80]
        print(f'  {path}: HTTP {e.code} - {body}')
    except Exception as e:
        print(f'  {path}: {e}')

print('\n=== Done ===')
