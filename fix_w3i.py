# Fix web3 module - remove problematic CSRF import
with open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the problematic import
content = content.replace(
    'from flask_wtf.csrf import CSRFProtect, csrf_exempt\n',
    ''
)
# Remove @csrf_exempt decorator
content = content.replace(
    '@csrf_exempt\n',
    ''
)

with open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Add csrf exemption in main.py instead
with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

# Find where web3_bp is registered and add csrf exemption after it
old_reg = "app.register_blueprint(web3_bp)"
new_reg = """app.register_blueprint(web3_bp)
# CSRF exemption for web3 endpoints
csrf.exempt(web3_bp.view_functions.get('web3_bp.web3_info'))
csrf.exempt(web3_bp.view_functions.get('web3_bp.web3_send'))
csrf.exempt(web3_bp.view_functions.get('web3_bp.web3_history'))"""

main_content = main_content.replace(old_reg, new_reg)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(main_content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('Web3 module: Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Web3 module: {e}')

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Main.py: Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Main.py: {e}')
