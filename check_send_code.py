import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Find and print the web3_send function
lines = w3.split('\n')
in_send = False
for i, line in enumerate(lines):
    if 'def web3_send' in line:
        in_send = True
    if in_send:
        print(f'L{i+1}: {line}')
        if in_send and line.strip() == '' and i > 0 and lines[i-1].strip().endswith('})'):
            break
    if in_send and i > 50:
        break
