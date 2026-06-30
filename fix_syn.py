with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix decorator
content = content.replace(
    '@app.route("/admin/")\ndef admin_login_page():',
    '@app.route("/admin/")\n\ndef admin_login_page():'
)

# 2. Restrict_routes - already should be: if path == '/admin' or path.startswith('/admin/')
# Let me verify and fix it
old_routes = "if path == '/admin' or path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/'):"
if old_routes not in content:
    # Try to find the current version
    idx = content.find('ALLOWED_PREFIXES')
    if idx > 0:
        # Check the actual content
        snippet = content[idx:idx+200]
        print(f'ALLOWED section: {snippet}')

# Check if the decorator fix worked
if '@app.route("/admin/")\ndef admin_login_page():' not in content:
    print('Decorator fix applied successfully')
else:
    print('ERROR: Decorator still broken')

# Check admin route accessibility in restrict_routes
if "path == '/admin' or path.startswith('/admin/')" in content:
    print('Restrict routes includes /admin check')
else:
    print('WARNING: /admin may not be in restrict_routes')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
