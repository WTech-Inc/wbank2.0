import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
old = "if path == '/' or path == '/wbank' or path.startswith('/wbank/'):"
new = "if path == '/' or path == '/wbank' or path.startswith('/wbank/') or path == '/auth/reg' or path.startswith('/auth/'):"
m = m.replace(old, new)
open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)
print('[OK] Routes fixed')

import py_compile
py_compile.compile('E:\\wbank\\main.py', doraise=True)
print('[OK] Syntax OK')

# Verify
lines = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'auth/reg' in line and 'startswith' in line:
        print(f'L{i+1}: {line.strip()}')
