with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace exempt_blueprint with direct set manipulation
content = content.replace(
    "csrf.exempt_blueprint(web3_bp)",
    "csrf._exempt_blueprints.add('web3_bp')"
)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
