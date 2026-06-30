"""Add gasless WTC send - match current code exactly"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

GAS_FEE = 50

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
lines = w3.split('\n')

# Find the exact send function boundaries
print('=== Scanning web3_send function ===')
start = -1
for i, line in enumerate(lines):
    if 'def web3_send' in line:
        start = i
        break

if start < 0:
    print('ERROR: web3_send not found')
    sys.exit(1)

# Print the full function
print(f'Send function starts at line {start+1}')
for j in range(start, min(start+40, len(lines))):
    print(f'L{j+1}: {lines[j]}')

print('\n=== Find exact patterns ===')
# Show key sections
for keyword in ['Insufficient balance', 'total_cost', 'FIRST', 'ERC20 WTC', 'Record transaction', '"success": True']:
    for i, line in enumerate(lines):
        if keyword in line:
            print(f'L{i+1}: {line.strip()[:120]}')
            break
