"""Balance braces in script blocks"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()
lines = tpl.split('\n')

# Block 1: lines 8-204 (0-indexed: 7-203)
# Block 2: lines 1086-1717 (0-indexed: 1085-1716)

print('=== Block 1 (lines 8-204) ===')
block1 = '\n'.join(lines[7:204])
ob1 = block1.count('{') - block1.count('}')
print(f'Balance: {ob1} (should be 0, currently -1)')

# Find the extra } in block 1
if ob1 < 0:
    # Check each line
    bal = 0
    for i in range(7, 204):
        bal += lines[i].count('{') - lines[i].count('}')
        if bal < 0:
            print(f'  First negative at L{i+1}: {lines[i].strip()[:80]}')
            # Remove this line's extra }
            new_line = lines[i].replace('}', '', 1)
            print(f'  Fixed: {new_line.strip()[:80]}')
            lines[i] = new_line
            break

print('\n=== Block 2 (lines 1086-1717) ===')
block2 = '\n'.join(lines[1085:1717])
ob2 = block2.count('{') - block2.count('}')
print(f'Balance: {ob2} (should be 0, currently -1)')

if ob2 < 0:
    bal = 0
    for i in range(1085, 1717):
        bal += lines[i].count('{') - lines[i].count('}')
        if bal < 0:
            print(f'  First negative at L{i+1}: {lines[i].strip()[:80]}')
            # Remove this line's extra }
            new_line = lines[i].replace('}', '', 1)
            print(f'  Fixed: {new_line.strip()[:80]}')
            lines[i] = new_line
            break

# Also remove orphaned "};" lines that are immediately followed by another function or }
print('\n=== Removing orphaned "};" lines ===')
removed = 0
for i in range(len(lines)-1):
    stripped = lines[i].strip()
    if stripped == '};':
        # Check if next non-empty line starts a new function or is closing
        next_non_empty = ''
        for j in range(i+1, min(i+5, len(lines))):
            if lines[j].strip():
                next_non_empty = lines[j].strip()
                break
        # If next non-empty specifies an unrelated function/var, this is orphaned
        if next_non_empty.startswith('const ') or next_non_empty == 'function showPage':
            # This is an orphaned }; from a removed showPage override
            lines[i] = ''
            removed += 1
            print(f'  Removed L{i+1} (next: {next_non_empty[:40]})')

# Write back
result = '\n'.join(lines)
open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8').write(result)
print(f'\n[OK] Removed {removed} orphaned braces')

# Final balance check
new_tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()
for idx_start, idx_end, name in [(7, 204, 'Block1'), (1085, 1717, 'Block2')]:
    block = '\n'.join(new_tpl.split('\n')[idx_start:idx_end])
    bal = block.count('{') - block.count('}')
    print(f'{name} balance: {bal}')
