import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
for line in w3.split('\n'):
    if 'RPC' in line or 'http' in line.lower() or 'CHAIN' in line or 'network' in line:
        print(line.strip()[:150])
