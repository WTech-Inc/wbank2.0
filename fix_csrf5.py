with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the old exempt block (after csrf = CSRFProtect)
import re
content = re.sub(
    r"# Mark all web3 views as csrf exempt\nfor rule in app\.url_map\.iter_rules\(\):\n    if 'web3_bp' in rule\.endpoint:\n        try:\n            app\.view_functions\[rule\.endpoint\]\._csrf_exempt = True\n        except:\n            pass\n",
    '',
    content
)

# Add a proper csrf exempt after csrf = CSRFProtect(app)
old_csrf = 'csrf = CSRFProtect(app)'
new_csrf = """csrf = CSRFProtect(app)

# CSRF exempt for web3 blueprint views
csrf.exempt(web3_bp.view_functions.get('web3_bp.web3_info'))
csrf.exempt(web3_bp.view_functions.get('web3_bp.web3_send'))
csrf.exempt(web3_bp.view_functions.get('web3_bp.web3_history'))
"""

content = content.replace(old_csrf, new_csrf)

# Remove the extra restrict_routes check
content = content.replace(
    "    if request.path.startswith(\"/wbank/web3/\"):\n        return None\n",
    ''
)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
