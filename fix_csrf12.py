import py_compile, re

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove ALL old csrf hack code
content = re.sub(r"\n# Correct CSRF exempt for web3 views\n.*?pass\n", '\n', content, flags=re.DOTALL)
content = re.sub(r"\n# CSRF exemption for web3 blueprint endpoints\n.*?pass\n", '\n', content, flags=re.DOTALL)
content = re.sub(r"\ncsrf\.exempt_blueprint\(.*?\)\n", '\n', content)
content = re.sub(r"\ncsrf\._exempt_blueprints\.add\(.*?\)\n", '\n', content)
content = re.sub(r"    # Bypass CSRF for web3 endpoints\n.*?_csrf_disable = True\n", '', content)
content = re.sub(r"# Disable CSRF for web3 routes dynamically\n.*?True\n", '', content, flags=re.DOTALL)
content = re.sub(r"# CSRF exemption for web3 routes - override via restirct_routes\npass\n", '', content)

# Monkey-patch csrf._is_exempt to skip web3 paths entirely
old_protect = 'csrf = CSRFProtect(app)\n'
new_protect = '''csrf = CSRFProtect(app)
# Monkey-patch _is_exempt for web3 paths (bypass CSRF entirely)
_orig_is_exempt = csrf._is_exempt
def _patched_is_exempt(self):
    if request.path.startswith('/wbank/web3/'):
        return True
    return _orig_is_exempt(self)
csrf._is_exempt = _patched_is_exempt.__get__(csrf, type(csrf))
'''
content = content.replace(old_protect, new_protect)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
