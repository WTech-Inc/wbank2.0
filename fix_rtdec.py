with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken route decorator
content = content.replace(
    '@app.route("/admin/")\ndef admin_login_page():',
    '@app.route("/admin/")\n\ndef admin_login_page():'
)

# Also fix the restrict_routes ALLOWED check
content = content.replace(
    "if path == '/admin' or path.startswith('/admin/') or path.startswith('/static/')",
    "if path.startswith('/admin/') or path.startswith('/static/')"
)

# Instead of the broken duplicate /admin route, remove it - the /admin route already exists
# Check for duplicate
import re
admin_routes = [m.start() for m in re.finditer(r"@app\.route\(\"/admin\"\)", content)]
print(f'Found {len(admin_routes)} @app.route("/admin") decorators')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed route decorator')
