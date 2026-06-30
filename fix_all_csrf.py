"""Fix all missing CSRF exemptions"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# 1. Fix login route - add @csrf.exempt
old_login = '''@app.route("/wbank/auth/v1/session",methods=["GET","POST"])
def wbank_v1_auth_session():'''
new_login = '''@app.route("/wbank/auth/v1/session",methods=["GET","POST"])
@csrf.exempt
def wbank_v1_auth_session():'''

if old_login in m:
    m = m.replace(old_login, new_login)
    print('[OK] Login route CSRF exempt restored')
else:
    print('[WARN] Login route pattern not found')
    # Debug
    idx = m.find('wbank_v1_auth_session')
    if idx >= 0:
        print(f'Found at {idx}: ...{m[idx-60:idx+60]}')

# 2. Also fix the admin login route
old_admin = '''@app.route("/admin/login", methods=["POST"])
def admin_login():'''
new_admin = '''@app.route("/admin/login", methods=["POST"])
@csrf.exempt
def admin_login():'''
if old_admin in m:
    m = m.replace(old_admin, new_admin)
    print('[OK] Admin login CSRF exempt restored')

# Save
open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

import py_compile
py_compile.compile('E:\\wbank\\main.py', doraise=True)
print('[OK] Syntax OK')

print('\n=== Restart server ===')
