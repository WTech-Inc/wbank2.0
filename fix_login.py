import py_compile

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check what's there
idx = content.find('register_blueprint(web3_bp)')
if idx >= 0:
    print(f'web3_bp registration at {idx}')
    print(content[idx:idx+200])

# Fix: remove any broken csrf_token lines and add proper one
# Remove existing generate_csrf imports and jinja setup in wrong places
import re
content = re.sub(
    r"\nfrom flask_wtf\.csrf import generate_csrf\napp\.jinja_env\.globals\[\"csrf_token\"\] = generate_csrf",
    '',
    content
)

# Add proper csrf_token as a simple function
content = content.replace(
    "app.register_blueprint(web3_bp)\n",
    "app.register_blueprint(web3_bp)\n# Simple csrf_token for templates (CSRF bypassed)\nfrom flask_wtf.csrf import generate_csrf\napp.jinja_env.globals['csrf_token'] = generate_csrf\n"
)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
