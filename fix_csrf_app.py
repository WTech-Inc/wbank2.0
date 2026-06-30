import py_compile

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: use app.view_functions instead of web3_bp.view_functions
content = content.replace(
    "vf = web3_bp.view_functions.get(_n)",
    "vf = app.view_functions.get('web3_bp.' + _n)"
)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
