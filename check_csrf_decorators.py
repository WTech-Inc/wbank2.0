import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
lines = m.split('\n')

# Check csrf.exempt decorators
print('=== csrf.exempt decorators ===')
for i, line in enumerate(lines):
    if 'csrf.exempt' in line or 'csrf_exempt' in line or 'CSRFProtect' in line:
        print(f'L{i+1}: {line.strip()[:100]}')

print()
print('=== Login route check ===')
for i, line in enumerate(lines):
    if 'v1/session' in line or 'wbank_v1_auth_session' in line:
        for j in range(max(0,i-2), min(len(lines), i+3)):
            print(f'L{j+1}: {lines[j]}')
        print('---')

print()
print('=== Web3 routes csrf check ===')
for i, line in enumerate(lines):
    if 'web3_bp' in line and ('csrf' in line.lower() or 'exempt' in line.lower() or 'for' in line.lower()):
        for j in range(max(0,i-1), min(len(lines), i+4)):
            print(f'L{j+1}: {lines[j]}')
        print('---')
