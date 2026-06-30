import py_compile, re

# The SIMPLEST correct fix
with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Clean up old broken code
content = re.sub(
    r"\n# CSRF exemption for web3 blueprint endpoints\n.*?pass\n",
    '\n',
    content,
    flags=re.DOTALL
)
content = re.sub(r"\ncsrf\.exempt_blueprint\(.*?\)\n", '\n', content)
content = re.sub(r"\ncsrf\._exempt_blueprints\.add\(.*?\)\n", '\n', content)
content = content.replace(
    "    # Bypass CSRF for web3 endpoints\n        if request.path.startswith('/wbank/web3/'):\n            from flask_wtf.csrf import generate_csrf\n            request._csrf_disable = True\n",
    ''
)
content = re.sub(
    r"# Disable CSRF for web3 routes dynamically\n_orig_csrf_protect = None.*?\._csrf_exempt = True\n",
    '',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r"# CSRF exemption for web3 routes - override via restirct_routes\npass\n",
    '',
    content
)

# Add CORRECT fix
old_csrf = 'csrf = CSRFProtect(app)\n'
new_csrf = 'csrf = CSRFProtect(app)\n# Correct CSRF exempt for web3 views\nfor _name in [\'web3_info\', \'web3_send\', \'web3_history\']:\n    try:\n        vf = web3_bp.view_functions.get(_name)\n        if vf:\n            csrf.exempt(vf)\n    except Exception:\n        pass\n'

content = content.replace(old_csrf, new_csrf)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Main.py: Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Main.py: {e}')
