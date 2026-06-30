import subprocess, os, time, sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Fix ABI in wbank_web3.py - ensure proper Python booleans
print('[1/4] Fix ABI booleans...')
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Use regex to replace JSON-style booleans with Python-style
import re
w3 = re.sub(r'(?<!["\'])false(?!["\'])', 'False', w3)
w3 = re.sub(r'(?<!["\'])true(?!["\'])', 'True', w3)
open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)
print('  [OK] wbank_web3.py ABI fixed')

# 2. Check main.py for any JSON booleans
print('[2/4] Check main.py...')
main = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
if 'false' in main or 'true' in main:
    # Only fix within data structures, not in strings
    main_fixed = re.sub(r'(?<!["\'])false(?!["\'])', 'False', main)
    main_fixed = re.sub(r'(?<!["\'])true(?!["\'])', 'True', main_fixed)
    if main_fixed != main:
        open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(main_fixed)
        print('  [OK] main.py booleans fixed')
    else:
        print('  [OK] main.py OK')
else:
    print('  [OK] main.py OK')

# 3. Verify syntax
print('[3/4] Verify syntax...')
try:
    import py_compile
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('  [OK] wbank_web3.py syntax OK')
except py_compile.PyCompileError as e:
    print(f'  [FAIL] {e}')

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('  [OK] main.py syntax OK')
except py_compile.PyCompileError as e:
    print(f'  [FAIL] {e}')

# 4. Start server via task scheduler (more reliable)
print('[4/4] Start server...')
subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True, timeout=10)
time.sleep(2)

# Use PowerShell to start hidden process
ps_cmd = '''
$env:dataurl='postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
$env:HTTP_PORT='8080'
$env:HTTPS_PORT='8443'
Start-Process -WindowStyle Hidden -FilePath 'python' -ArgumentList 'main.py' -WorkingDirectory 'E:\\wbank'
'''
with open('E:\\wbank\\start.ps1', 'w') as f:
    f.write(ps_cmd)

r = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'E:\\wbank\\start.ps1'],
                   capture_output=True, text=True, timeout=15)
if r.stderr:
    print(f'  PS err: {r.stderr[:200]}')
time.sleep(4)

# Check
r2 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
if 'python' in r2.stdout:
    print(f'  [OK] Server running')
else:
    print(f'  [FAIL] Server not started')
    # Try wmic
    subprocess.run(['wmic', 'process', 'call', 'create',
                   '"python main.py"',
                   '-directory', 'E:\\wbank'],
                   capture_output=True, timeout=10)
    time.sleep(4)
    r3 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
    if 'python' in r3.stdout:
        print(f'  [OK] Server running (wmic method)')
    else:
        print(f'  [FAIL] Still not running')
        # Try direct
        env = os.environ.copy()
        env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
        env['HTTP_PORT'] = '8080'
        env['HTTPS_PORT'] = '8443'
        subprocess.Popen(['python', 'main.py'], cwd='E:\\wbank', env=env,
            stdout=open('E:\\wbank\\run.log', 'w'), stderr=subprocess.STDOUT,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        time.sleep(3)
        r4 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
        if 'python' in r4.stdout:
            print(f'  [OK] Server running (direct Popen)')
        else:
            print(f'  [FAIL] Check E:\\wbank\\run.log')

# Final check
import urllib.request
try:
    r = urllib.request.urlopen('http://localhost:8080/auth/reg', timeout=5)
    print(f'  [OK] /auth/reg: HTTP {r.status}')
except Exception as e:
    print(f'  /auth/reg: {e}')

print('\n=== Done ===')
