"""Fix admin route blocked by before_request"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Fix the before_request handler for /admin
old = "if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/'):"
new = "if path == '/admin' or path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/'):"

if old in m:
    m = m.replace(old, new)
    print('[OK] Admin route unblocked (/admin + /admin/*)')
else:
    print('[WARN] Pattern not found, checking...')
    for i, line in enumerate(m.split('\n')):
        if 'admin' in line and 'startswith' in line:
            print(f'L{i+1}: {line.strip()}')

open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

import py_compile
py_compile.compile('E:\\wbank\\main.py', doraise=True)
print('[OK] Syntax OK')
print('\nRestart server')
