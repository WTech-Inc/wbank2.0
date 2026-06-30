with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and remove the old broken csrf exempt block
old = '''# CSRF exemption for web3 blueprint endpoints
for _f in ['web3_bp.web3_info', 'web3_bp.web3_send', 'web3_bp.web3_history']:
    try:
        csrf.exempt(web3_bp.view_functions[_f])
    except:
        pass'''

new = '''# CSRF exemption for web3 blueprint (by endpoint string)
csrf.exempt('web3_bp.web3_info')
csrf.exempt('web3_bp.web3_send')
csrf.exempt('web3_bp.web3_history')'''

if old in content:
    content = content.replace(old, new)
    print('CSRF exemption fixed')
else:
    print('Could not find old CSRF block')
    # Show what's there
    idx = content.find('CSRF exemption for web3')
    if idx >= 0:
        print(content[idx:idx+300])

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
