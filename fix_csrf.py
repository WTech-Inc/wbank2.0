with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add @csrf.exempt to admin login route
content = content.replace(
    '@app.route("/admin/login", methods=["POST"])\ndef admin_login():',
    '@app.route("/admin/login", methods=["POST"])\n@csrf.exempt\ndef admin_login():'
)

# Also exempt the audit_log, stats, users API endpoints
for route in ['admin_api_stats', 'admin_api_audit_log', 'admin_api_users',
              'admin_api_verify_user', 'admin_api_freeze_user', 'admin_api_update_balance']:
    old = f'def {route}():'
    new = f'@csrf.exempt\ndef {route}():'
    content = content.replace(old, new)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')

# Verify routes
count = content.count('@csrf.exempt')
print(f'Added @csrf.exempt to {count} routes')
