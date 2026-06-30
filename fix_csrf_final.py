import py_compile

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add @csrf.exempt to the V1 login session route
old1 = 'def wbank_v1_auth_session():'
new1 = '@csrf.exempt\ndef wbank_v1_auth_session():'
content = content.replace(old1, new1)

# Add to admin login
old2 = 'def admin_login():'
# Only the FIRST occurrence - the one for admin, not the old one
# Find the admin one (has """Admin login handler)
idx = content.find('def admin_login():')
# Replace only this one
content = content[:idx] + '@csrf.exempt\n' + content[idx:]

# Add CSRF exempt to web3 send endpoint via app.view_functions after csrf init
# Find where csrf = CSRFProtect is and add exempt after it
old_csrf = 'csrf = CSRFProtect(app)'
new_csrf = old_csrf + '\n# CSRF exempt for web3 views\nfor _n in ["web3_info", "web3_send", "web3_history"]:\n    vf = web3_bp.view_functions.get(_n)\n    if vf:\n        csrf.exempt(vf)\n'
content = content.replace(old_csrf, new_csrf)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
