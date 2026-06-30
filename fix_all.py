import py_compile

# 1. Fix pytz in web3 module
with open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8') as f:
    w3 = f.read()

if 'import pytz' not in w3:
    w3 = w3.replace(
        'import os, json, hashlib, datetime, base64',
        'import os, json, hashlib, datetime, base64, pytz'
    )
    print('Added pytz import')

with open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8') as f:
    f.write(w3)

# 2. Restore CSRFProtect properly
with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    main = f.read()

# Check if csrf = CSRFProtect exists
if 'CSRFProtect(app)' not in main:
    # Re-add CSRF
    # Find a good place - after app.config
    idx = main.find("app.config['UPLOAD_FOLDER']")
    if idx > 0:
        idx = main.find('\n', idx)
        insert = "\nfrom flask_wtf.csrf import CSRFProtect, generate_csrf\ncsrf = CSRFProtect(app)\n"
        main = main[:idx+1] + insert + main[idx+1:]
        print('Re-added CSRFProtect')

# Remove any duplicate generate_csrf imports
main_lines = main.split('\n')
seen = set()
clean = []
in_imports = False
for line in main_lines:
    if 'from flask_wtf.csrf import generate_csrf' in line and 'generate_csrf' in seen:
        continue  # Skip duplicate
    if 'generate_csrf' in line:
        seen.add('generate_csrf')
    clean.append(line)
main = '\n'.join(clean)

# Add CSRF exemption for web3 using blueprint method
# Find csrf = CSRFProtect(app) and add exemption after it
old = 'csrf = CSRFProtect(app)'
if old in main:
    new = old + '\n# CSRF exempt for web3 blueprint\nfor _name in [\'web3_info\', \'web3_send\', \'web3_history\']:\n    try:\n        vf = web3_bp.view_functions.get(_name)\n        if vf:\n            csrf.exempt(vf)\n    except:\n        pass\n'
    main = main.replace(old, new)
    print('Added CSRF exemption for web3')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(main)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Main.py: Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Main.py: {e}')

try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('Web3 module: Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Web3 module: {e}')
