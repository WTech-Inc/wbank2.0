"""Fix admin 500 errors - template and CSRF"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Check admin login route
lines = m.split('\n')
print('=== Admin routes ===')
for i, line in enumerate(lines):
    if '/admin' in line and ('@app.route' in line or 'def admin' in line):
        print(f'L{i+1}: {line.strip()[:120]}')
        # Print next 2 lines for context
        for j in range(1, 4):
            if i+j < len(lines):
                l = lines[i+j].strip()
                if l:
                    print(f'  L{i+j+1}: {l[:120]}')
        print()

# Check admin login has methods POST
print('=== Fixing admin login ===')
old_admin_login = '''@app.route("/admin/login", methods=["POST"])
def admin_login():'''
new_admin_login = '''@app.route("/admin/login", methods=["POST"])
@csrf.exempt
def admin_login():'''

if old_admin_login in m:
    m = m.replace(old_admin_login, new_admin_login)
    print('[OK] Added @csrf.exempt to admin login')
elif '@csrf.exempt' in m and 'admin_login' in m:
    print('[OK] Already has csrf.exempt')

# Check admin template exists
print('\n=== Admin template ===')
import os
tpl_path = 'E:\\wbank\\templates\\admin\\index.html'
if os.path.exists(tpl_path):
    print(f'[OK] Admin template exists ({os.path.getsize(tpl_path)} bytes)')
else:
    print(f'[WARN] Admin template missing at {tpl_path}')
    # Try to find it
    for root, dirs, files in os.walk('E:\\wbank\\templates'):
        for f in files:
            if 'admin' in f.lower() or 'index' in f.lower():
                print(f'  Found: {os.path.join(root, f)}')

# Write main.py back
open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

import py_compile
py_compile.compile('E:\\wbank\\main.py', doraise=True)
print('[OK] Syntax OK')
print('\nRestart server')
