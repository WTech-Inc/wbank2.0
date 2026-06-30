import sys
sys.stdout.reconfigure(encoding='utf-8')

c = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
print('auth/reg route:', '/auth/reg' in c)
print('register_page def:', 'def register_page' in c)
print('register_submit def:', 'def register_submit' in c)
print('KYC SQL:', 'INSERT INTO wbankkyc' in c)
print('File size:', len(c), 'bytes')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
print('ERC20 transfer:', 'ERC20 WTC Transfer' in w3)
print('WTC_CONTRACT_ADDRESS:', 'WTC_CONTRACT_ADDRESS' in w3)

import subprocess, time
time.sleep(3)
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], capture_output=True, text=True, timeout=10)
print('Python processes:', result.stdout.count('python.exe'))

# Check if the server is responding
import urllib.request
for url in ['/auth/reg', '/wbank', '/wbank/auth/v1']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{url}', timeout=5)
        print(f'{url}: HTTP {r.status}')
    except Exception as e:
        print(f'{url}: {e}')
