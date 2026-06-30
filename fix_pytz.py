with open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add pytz import
content = content.replace(
    'import os, json, hashlib, datetime, base64',
    'import os, json, hashlib, datetime, base64, pytz'
)

with open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')

# Verify
c = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
print('pytz imported:', 'pytz' in c)
