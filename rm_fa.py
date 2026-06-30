with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = 0
remove_ranges = []

for i, line in enumerate(lines):
    # Remove any Admin() instantiation from Flask-Admin
    if 'Admin(app, name=' in line or 'Admin(app, index_view=' in line:
        lines[i] = ''
        changes += 1
        print(f'Removed Admin() at line {i+1}')

    # Remove Flask-Admin import lines
    if line.strip().startswith('from flask_admin') or line.strip().startswith('import flask_admin'):
        lines[i] = ''
        changes += 1
        print(f'Removed flask_admin import at line {i+1}')

    # Remove any Admin view registrations
    if 'admin.add_view(' in line or 'admin.add_view(View(' in line:
        lines[i] = ''
        changes += 1
        print(f'Removed admin view at line {i+1}')

    # Remove Flask-Admin config
    if 'FLASK_ADMIN' in line:
        lines[i] = ''
        changes += 1
        print(f'Removed FLASK_ADMIN config at line {i+1}')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')

print(f'Changes: {changes}')
