with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find restrict_routes function and fix the admin path check
in_restrict = False
for i, line in enumerate(lines):
    if 'def restrict_routes' in line:
        in_restrict = True
    if in_restrict and "if path.startswith('/admin/')" in line:
        lines[i] = line.replace("if path.startswith('/admin/')", "if path == '/admin' or path.startswith('/admin/')")
        print(f'Fixed line {i+1}')
        break
    if in_restrict and line.strip().startswith('@app.after_request') or line.strip().startswith('def '):
        if line.strip() != 'def restrict_routes():':
            in_restrict = False

# Also add the trailing slash route for /admin
for i, line in enumerate(lines):
    if "@app.route('/admin')" in line or '@app.route("/admin")' in line:
        lines[i] = line.rstrip() + '\n@app.route("/admin/")'
        print(f'Added /admin/ route at line {i+1}')
        break

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Done - fixes applied')
