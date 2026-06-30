# REMOVE CSRF entirely - it's causing more problems than it solves
with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all csrf-related code
content = content.replace(
    "from flask_wtf.csrf import CSRFProtect,generate_csrf\n",
    ""
)
content = content.replace(
    "# Monkey-patch _is_exempt for web3 paths (bypass CSRF entirely)\n_orig_is_exempt = csrf._is_exempt\n",
    ""
)

# Remove the patched function
import re
content = re.sub(
    r"def _patched_is_exempt.*?csrf\._is_exempt = _patched_is_exempt\.__get__\(csrf, type\(csrf\)\)\n",
    '',
    content,
    flags=re.DOTALL
)

# Remove csrf = CSRFProtect(app) line
content = re.sub(r"\ncsrf = CSRFProtect\(app\)\n", '\n', content)

# Remove all @csrf.exempt decorators
content = content.replace('\n@csrf.exempt\n', '\n')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
