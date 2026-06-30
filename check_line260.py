import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
lines = m.split('\n')
for i in range(255, 270):
    if i < len(lines):
        print(f'L{i+1}: {lines[i][:120]}')
