"""Fix WTC ABI - replace JSON true/false with Python True/False"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Fix wbank_web3.py
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
# Replace JSON booleans with Python booleans in the ABI
w3 = w3.replace(': false', ': False')
w3 = w3.replace(': false,', ': False,')
w3 = w3.replace(': true', ': True')
w3 = w3.replace(': true,', ': True,')
open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)
print('[OK] ABI fixed')

# Now start the server using a technique that works via SSH
import subprocess, os, time

# Kill old
subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True, timeout=10)
time.sleep(2)

# Write a VBS script to start server (more reliable via SSH)
vbs = '''
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "E:\\wbank"
WshShell.Run "python main.py", 0, False
'''

with open('E:\\wbank\\start_server.vbs', 'w') as f:
    f.write(vbs)

# Run VBS
subprocess.run(['cscript', '//nologo', 'E:\\wbank\\start_server.vbs'], capture_output=True, timeout=10)
time.sleep(3)

# Verify
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
if 'python' in r.stdout:
    print(f'[OK] Server started')
else:
    print(f'[FAIL] Server not running')
    # Check log
    try:
        log = open('E:\\wbank\\run.log', 'r', encoding='utf-8').read()
        print('LOG:', log[-500:])
    except Exception as e:
        print(f'Log error: {e}')

# Check auth/reg
import urllib.request
try:
    r = urllib.request.urlopen('http://localhost:8080/auth/reg', timeout=5)
    print(f'[OK] /auth/reg: HTTP {r.status}')
except Exception as e:
    print(f'/auth/reg check: {e}')
