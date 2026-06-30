"""Find and fix ALL stray braces in the template"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()
lines = tpl.split('\n')

# Check lines around 1635
print('=== Lines 1630-1640 ===')
for i in range(1625, 1645):
    if i < len(lines):
        print(f'L{i+1}: {lines[i]}')

# Count braces in script tags
in_script = False
brace_count = 0
open_braces = 0

for i, line in enumerate(lines):
    if '<script' in line and 'src=' not in line:
        in_script = True
    if '</script>' in line:
        in_script = False
    if in_script:
        open_braces += line.count('{')
        close_braces = line.count('}')
        brace_count += open_braces - close_braces

print(f'\n=== Script brace balance: {brace_count} (should be 0) ===')

# Find ALL script blocks and check brace balance
in_script_block = False
script_start = 0
block_balance = 0
for i, line in enumerate(lines):
    if '<script' in line and 'src=' not in line and '</script>' not in line:
        in_script_block = True
        script_start = i
        block_balance = 0
    if in_script_block:
        block_balance += line.count('{') - line.count('}')
    if '</script>' in line and in_script_block:
        if block_balance != 0:
            print(f'Braces unbalanced in script block L{script_start+1}-{i+1}: {block_balance}')
        in_script_block = False

# Find ALL "};" that are on their own line (common source of stray braces)
print('\n=== Stray "};" on own line ===')
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == '};' and i < len(lines) - 1:
        next_line = lines[i+1].strip()
        # If next line is also a closing brace or script end, it's a problem
        print(f'L{i+1}: }}; (next: "{next_line[:40]}")')
