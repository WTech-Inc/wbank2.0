# The SIMPLEST correct fix
with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Clean up all old broken code
import re
# Remove the broken loop block
content = re.sub(
    r"\n# CSRF exemption for web3 blueprint endpoints\nfor _f in \[.*?\]\.split\('.+?\)\n    try:\n        .*?\n    except:\n        pass\n",
    '\n',
    content,
    flags=re.DOTALL
)

# Remove any stray csrf.exempt_blueprint or csrf._exempt_blueprints lines
content = re.sub(
    r"\ncsrf\.exempt_blueprint\(.*?\)\n",
    '\n',
    content
)
content = re.sub(
    r"\ncsrf\._exempt_blueprints\.add\(.*?\)\n",
    '\n',
    content
)

# Remove the override blocks
content = re.sub(
    r"# CSRF exemption for web3 routes - override via restirct_routes\npass\n",
    '\n',
    content
)
content = re.sub(
    r"# Bypass CSRF for web3 endpoints\n        if request\.path\.startswith\('/wbank/web3/'\):.*?request\._csrf_disable = True\n",
    '',
    content
)
content = re.sub(
    r"# Disable CSRF for web3 routes dynamically\n_orig_csrf_protect = None.*?app\.view_functions\[request\.endpoint\]\._csrf_exempt = True\n",
    '',
    content,
    flags=re.DOTALL
)

# Now add the CORRECT fix: use view_functions with the right key (without blueprint prefix)
old_csrf = 'csrf = CSRFProtect(app)\n'
new_csrf = 'csrf = CSRFProtect(app)\n# CSRF exempt for web3 views\nfor _name in [\'web3_info\', \'web3_send\', \'web3_history\']:\n    try:\n        vf = web3_bp.view_functions.get(_name)\n        if vf:\n            csrf.exempt(vf)\n    except:\n        pass\n'

content = content.replace(old_csrf, new_csrf)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')

# Also clean up wbank_web3.py - remove the _exempt_web3_views function
with open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8') as f:
    web3_content = f.read()

web3_content = re.sub(
    r"\n# CSRF exemption via current_app.*?pass\n",
    '',
    web3_content,
    flags=re.DOTALL
)

# Remove trailing _csrf_exempt lines
web3_content = re.sub(
    r"\nweb3_info\._csrf_exempt = True\nweb3_send\._csrf_exempt = True\nweb3_history\._csrf_exempt = True\n",
    '\n',
    web3_content
)

with open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8') as f:
    f.write(web3_content)

try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('Web3 module: Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Web3 module: {e}')
