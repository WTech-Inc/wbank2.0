import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
lines = m.split('\n')

for i, line in enumerate(lines):
    if 'v1/session' in line or 'wbank_v1_auth_session' in line:
        for j in range(max(0,i-3), min(len(lines), i+3)):
            print(f'L{j+1}: {lines[j]}')
        print()
