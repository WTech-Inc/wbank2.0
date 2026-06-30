"""Add gasless send - dynamic find and replace"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

GAS_FEE = 50

w = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
lines = w.split('\n')
changes = 0

# 1. Find and modify balance check
for i, line in enumerate(lines):
    if 'int(user.balance) < amount' in line and 'Insufficient' in line:
        lines[i] = line.replace(
            'int(user.balance) < amount',
            'int(user.balance) < total_amount'
        )
        lines[i] = lines[i].replace(
            '"Insufficient balance"',
            f'"Insufficient balance (need " + str(total_amount) + " WTC: " + str(amount) + " + {GAS_FEE} fee)"'
        )
        # Add total_amount before this line
        spacer = ' ' * (len(line) - len(line.lstrip()))
        lines.insert(i, spacer + 'total_amount = amount + ' + str(GAS_FEE))
        changes += 1
        print(f'[OK] Balance check: line {i+1}')
        break

# 2. Find and modify DB deduction
for i, line in enumerate(lines):
    if 'user.balance = str(int(user.balance) - amount)' in line:
        lines[i] = line.replace('amount', 'total_amount')
        changes += 1
        print(f'[OK] DB deduction: line {i+1}')
        break

# 3. Find and modify transaction record to add fee info
for i, line in enumerate(lines):
    if 'WTC Transfer: Sent' in line and 'Tx:' in line and 'Fee' not in line:
        lines[i] = line.replace(
            'f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}..."',
            'f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}... (Fee: ' + str(GAS_FEE) + ' WTC)"'
        )
        changes += 1
        print(f'[OK] TX record includes fee: line {i+1}')
        break

# 4. Find and modify return JSON
for i, line in enumerate(lines):
    if '"success": True' in line:
        # Add fee fields after success line
        insert_idx = i + 1
        spacer = ' ' * (len(lines[i]) - len(lines[i].lstrip()))
        lines.insert(insert_idx, spacer + '"fee": ' + str(GAS_FEE) + ',')
        lines.insert(insert_idx + 1, spacer + '"total_deducted": total_amount,')
        changes += 1
        print(f'[OK] Return JSON includes fee: line {i+1}')
        break

# Write back
result = '\n'.join(lines)
open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(result)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print(f'[OK] Syntax OK ({changes} changes)')
print(f'Gas fee: {GAS_FEE} WTC per tx')
