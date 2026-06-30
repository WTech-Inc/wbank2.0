import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

# Check what's listening on port 8080
r = subprocess.run(['netstat', '-ano', '|', 'findstr', ':8080'], capture_output=True, text=True, timeout=10, shell=True)
print('Port 8080:')
print(r.stdout[:500] if r.stdout else 'Nothing listening')

# Check all python processes
r2 = subprocess.run(['tasklist', '/V', '/FI', 'IMAGENAME eq python.exe'], capture_output=True, text=True, timeout=10, shell=True)
print('\nPython processes:')
print(r2.stdout[:500] if r2.stdout else 'None')

# Try to connect and check server headers
import urllib.request
try:
    r3 = urllib.request.urlopen('http://localhost:8080/', timeout=5)
    print(f'\nServer: {r3.headers.get("Server", "unknown")}')
    print(f'Date: {r3.headers.get("Date", "unknown")}')
except Exception as e:
    print(f'\nConnection error: {e}')
