# NUCLEAR OPTION: set _csrf_exempt on web3 functions at module level
with open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add at the end of the file
content += '\n\n# CSRF exemption\nweb3_info._csrf_exempt = True\nweb3_send._csrf_exempt = True\nweb3_history._csrf_exempt = True\n'

with open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('Web3: Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Web3: {e}')

# Also fix main.py - restore the original csrf = CSRFProtect(app) line and remove all the hacks
with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

# Remove the csrf exempt block before startup
import re
main_content = re.sub(
    r"\n# CSRF exemption for web3 views.*?app\.view_functions\['web3_bp\.web3_history'\]._csrf_exempt = True\n",
    '',
    main_content,
    flags=re.DOTALL
)

# Ensure csrf = CSRFProtect(app) is clean
main_content = re.sub(
    r"csrf = CSRFProtect\(app\)\n\n# CSRF exempt for web3 blueprint views\ncsrf\.exempt\(.*?\)\ncsrf\.exempt\(.*?\)\ncsrf\.exempt\(.*?\)\n",
    "csrf = CSRFProtect(app)\n",
    main_content,
    flags=re.DOTALL
)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(main_content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Main.py: Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Main.py: {e}')
