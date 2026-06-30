"""Remove all Flask-Admin code from main.py"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Show problem area
lines = m.split('\n')
for i in range(248, 270):
    if i < len(lines):
        print(f'L{i+1}: {lines[i][:120]}')

# Find ALL lines related to Flask-Admin
# Remove everything from "from flask_admin" to the end of admin setup
m = re.sub(
    r"from flask_admin.*?[\s\S]*?app\.config\['FLASK_ADMIN.*?\n[\s\S]*?admin\.add_view\(.*?\)[\s\S]*?(?=\n@app\.route|\n\ndef|\nif __name)",
    '',
    m,
    flags=re.DOTALL
)

# Also remove any standalone admin.add_view lines
m = re.sub(r"admin\.add_view\(.*?\)\s*\n", '', m)
m = re.sub(r"admin = Admin\(.*?\)\s*\n", '', m)

# Even more aggressive: remove any line with "admin.add_view" or "Admin(" or "FLASK_ADMIN"
lines = m.split('\n')
lines = [l for l in lines if 'admin.add_view' not in l.lower() and 'flask_admin' not in l.lower() and "FLASK_ADMIN" not in l]
m = '\n'.join(lines)

print('\nAfter fix:')
# Show the same area
lines = m.split('\n')
for i in range(248, 270):
    if i < len(lines):
        print(f'L{i+1}: {lines[i][:120]}')

import py_compile
try:
    with open('E:\\wbank\\main2.py', 'w', encoding='utf-8') as f:
        f.write(m)
    py_compile.compile('E:\\wbank\\main2.py', doraise=True)
    print('\nSyntax: OK')
    # Replace original
    import shutil
    shutil.move('E:\\wbank\\main2.py', 'E:\\wbank\\main.py')

    # Check routes
    m2 = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
    print(f'/auth/reg: {"YES" if "/auth/reg" in m2 else "NO"}')
    print(f'register_page: {"YES" if "def register_page" in m2 else "NO"}')

except py_compile.PyCompileError as e:
    print(f'\nSyntax: {e}')
