with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the csrf.exempt lines with proper ones that work
old = """app.register_blueprint(web3_bp)
# CSRF exemption for web3 endpoints
csrf.exempt(web3_bp.view_functions.get('web3_bp.web3_info'))
csrf.exempt(web3_bp.view_functions.get('web3_bp.web3_send'))
csrf.exempt(web3_bp.view_functions.get('web3_bp.web3_history'))"""

new = """app.register_blueprint(web3_bp)
# CSRF exemption for web3 endpoints - apply at app level after registration
from flask_wtf.csrf import generate_csrf
# csrf.exempt works as a function too
_csrf_exempt_funcs = ['web3_bp.web3_info', 'web3_bp.web3_send', 'web3_bp.web3_history']
for _f in _csrf_exempt_funcs:
    if _f in app.view_functions:
        csrf.exempt(app.view_functions[_f])"""

content = content.replace(old, new)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
