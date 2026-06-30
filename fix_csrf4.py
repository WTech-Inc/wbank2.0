with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the csrf.exempt code from the blueprint registration
content = content.replace("""
# CSRF exemption for web3 endpoints - apply at app level after registration
from flask_wtf.csrf import generate_csrf
# csrf.exempt works as a function too
_csrf_exempt_funcs = ['web3_bp.web3_info', 'web3_bp.web3_send', 'web3_bp.web3_history']
for _f in _csrf_exempt_funcs:
    if _f in app.view_functions:
        csrf.exempt(app.view_functions[_f])""", '')

# Add CSRF exemption AFTER csrf is defined
# Find where csrf = CSRFProtect(app) is
old_csrf = 'csrf = CSRFProtect(app)'
new_csrf = """csrf = CSRFProtect(app)
# CSRF exemption for web3 blueprint endpoints
for _f in ['web3_bp.web3_info', 'web3_bp.web3_send', 'web3_bp.web3_history']:
    try:
        csrf.exempt(web3_bp.view_functions[_f])
    except:
        pass
"""
content = content.replace(old_csrf, new_csrf)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
