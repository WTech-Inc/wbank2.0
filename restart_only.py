import subprocess, os, time, sys
sys.stdout.reconfigure(encoding='utf-8')

# Check routes
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
print('register_page count:', m.count('def register_page'))
print('Has auth/reg:', '/auth/reg' in m)

# Kill
subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True, timeout=10)
time.sleep(2)

# Start via wmic (most reliable for remote)
result = subprocess.run([
    'wmic', 'process', 'call', 'create',
    'E:\\wbank\\main.py',
    '-directory', 'E:\\wbank'
], capture_output=True, text=True, timeout=15)

if result.returncode == 0:
    print('Server start command sent via wmic')
else:
    print(f'wmic error: {result.stderr}')
    # Fallback to file-based approach
    with open('E:\\wbank\\start.bat', 'w') as f:
        f.write('@echo off\n')
        f.write('cd /d E:\\wbank\n')
        f.write('set dataurl=postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require\n')
        f.write('set HTTP_PORT=8080\n')
        f.write('set HTTPS_PORT=8443\n')
        f.write('start /B python main.py > run.log 2>&1\n')
    subprocess.run(['start', 'E:\\wbank\\start.bat'], shell=True, capture_output=True, timeout=5)

time.sleep(5)

# Check
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
running = 'python' in r.stdout
print('Server running:', running)

# Test routes
import urllib.request
for path in ['/', '/auth/reg', '/wbank/auth/v1']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=5)
        print(f'  {path}: HTTP {r.status}')
    except urllib.error.HTTPError as e:
        print(f'  {path}: HTTP {e.code}')
    except Exception as e:
        print(f'  {path}: {e}')

# Check log for errors
log = open('E:\\wbank\\run.log', 'r', encoding='utf-8').read()
errors = [l for l in log.split('\n') if 'Traceback' in l or 'Error' in l or 'error' in l]
if errors:
    print(f'Log errors ({len(errors)}):')
    for e in errors[-3:]:
        print(f'  {e[:150]}')
else:
    print('No errors in log')
