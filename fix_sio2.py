with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix HTTP socketio.run line
content = content.replace(
    'allow_unsafe_werkzeug=True, use_debugger=False, use_reloader=False)',
    'allow_unsafe_werkzeug=True)'
)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')

# Verify
with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    ct = f.read()
print('use_debugger still present:', 'use_debugger' in ct)
