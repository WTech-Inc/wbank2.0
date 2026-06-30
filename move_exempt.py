import py_compile

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Move CSRF exemption to AFTER blueprint registration
# Remove the old exemption block (between csrf = CSRFProtect and auth)
old_exempt = """# CSRF exempt for web3 views
for _n in [\"web3_info\", \"web3_send\", \"web3_history\"]:
    vf = web3_bp.view_functions.get(_n)
    if vf:
        csrf.exempt(vf)
"""

# Remove ALL old exemption blocks
while old_exempt in content:
    content = content.replace(old_exempt, '')

# Also remove any other variants
import re
content = re.sub(r'\n# CSRF exempt for web3.*?pass\n', '\n', content, flags=re.DOTALL)
content = re.sub(r'\n# CSRF exemption for web3 blueprint.*?pass\n', '\n', content, flags=re.DOTALL)
content = re.sub(r'\nfor _n in \[.*?\n        pass\n', '\n', content, flags=re.DOTALL)

# Add proper exemption AFTER blueprint registration
old_reg = 'app.register_blueprint(web3_bp) # 註冊 Blueprint 並設定 URL 前綴'
new_reg = old_reg + '\n# CSRF exempt for web3 views (after blueprint registration)\nfor _n in ["web3_info", "web3_send", "web3_history"]:\n    vf = web3_bp.view_functions.get(_n)\n    if vf:\n        csrf.exempt(vf)\n'
content = content.replace(old_reg, new_reg)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
