import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
lines = w3.split('\n')

print('=== Full wbank_web3.py ===')
for i, line in enumerate(lines):
    print(f'L{i+1}: {line}')
