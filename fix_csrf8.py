with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the csrf block with exempt_blueprint
old = """# CSRF exemption for web3 routes - override via restirct_routes
pass"""

new = """# Exempt entire web3_bp from CSRF
csrf.exempt_blueprint(web3_bp)"""

content = content.replace(old, new)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
