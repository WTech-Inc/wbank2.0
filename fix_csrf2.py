with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add @csrf.exempt to the 3 POST endpoints
content = content.replace(
    '@app.route("/admin/api/verify_user", methods=["POST"])\ndef admin_api_verify_user():',
    '@app.route("/admin/api/verify_user", methods=["POST"])\n@csrf.exempt\ndef admin_api_verify_user():'
)
content = content.replace(
    '@app.route("/admin/api/freeze_user", methods=["POST"])\ndef admin_api_freeze_user():',
    '@app.route("/admin/api/freeze_user", methods=["POST"])\n@csrf.exempt\ndef admin_api_freeze_user():'
)
content = content.replace(
    '@app.route("/admin/api/update_balance", methods=["POST"])\ndef admin_api_update_balance():',
    '@app.route("/admin/api/update_balance", methods=["POST"])\n@csrf.exempt\ndef admin_api_update_balance():'
)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
