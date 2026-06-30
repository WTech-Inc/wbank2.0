import sys
sys.stdout.reconfigure(encoding='utf-8')
w = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
lines = w.split('\n')
for i in range(117, min(170, len(lines))):
    print(f'L{i+1}: {lines[i]}')
