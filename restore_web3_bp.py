"""Re-register web3 blueprint in main.py + add pytz to wbank_web3.py"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Check main.py for wcloud pattern
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

if 'register_blueprint(web3_bp)' in m:
    print('[OK] web3_bp already registered')
else:
    # Find wcloud_bp registration
    if 'wcloud_bp' in m:
        print('[INFO] Found wcloud_bp, adding web3_bp alongside...')

        # Add import
        old_import = "from wcloud import wcloud_bp"
        if old_import in m:
            m = m.replace(old_import, old_import + "\nfrom wbank_web3 import web3_bp")
            print('  Added import')

        # Add blueprint registration
        old_reg = "app.register_blueprint(wcloud_bp, url_prefix='/wcloud')"
        if old_reg in m:
            m = m.replace(old_reg, old_reg + "\napp.register_blueprint(web3_bp)")
            print('  Added blueprint registration')
    else:
        print('[WARN] wcloud_bp not found either - searching for alternate insertion point')
        # Try adding near the end before start_web
        insert = m.find("def start_web():")
        if insert > 0:
            # Add both import and registration
            bp_code = '''
# Register web3 blueprint
from wbank_web3 import web3_bp
app.register_blueprint(web3_bp)
'''
            m = m[:insert] + bp_code + m[insert:]
            print('  Added web3_bp registration before start_web()')

    open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

    # Verify
    if 'register_blueprint(web3_bp)' in m:
        print('[OK] web3_bp now registered')
    else:
        print('[WARN] web3_bp still not registered')

# 2. Fix pytz in wbank_web3.py
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
if 'import pytz' not in w3:
    w3 = w3.replace('import hashlib, datetime', 'import hashlib, datetime, pytz')
    w3 = w3.replace('import datetime, base64', 'import datetime, base64, pytz')
    w3 = w3.replace('import datetime', 'import datetime, pytz')
    open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)
    print('[OK] pytz import added to wbank_web3.py')
else:
    print('[OK] pytz already in wbank_web3.py')

# 3. Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('[OK] main.py syntax OK')
except py_compile.PyCompileError as e:
    print(f'[FAIL] main.py: {e}')

try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('[OK] wbank_web3.py syntax OK')
except py_compile.PyCompileError as e:
    print(f'[FAIL] wbank_web3.py: {e}')

print('\n=== Restart server needed ===')
