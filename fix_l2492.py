with open('E:\\wbank\\main.py', 'rb') as f:
    lines = f.readlines()

# Line 2492 (index 2491) is broken: b'@app.route("/admin/")def admin_login_page():\r\n'
# Fix it to: b'@app.route("/admin/")\r\ndef admin_login_page():\r\n'
old_line = lines[2491]
new_line1 = b'@app.route("/admin/")\r\n'
new_line2 = b'def admin_login_page():\r\n'
lines[2491] = new_line1
lines.insert(2492, new_line2)

with open('E:\\wbank\\main.py', 'wb') as f:
    f.writelines(lines)

# Verify
print(f'Old line: {old_line}')
print(f'New lines: {new_line1}{new_line2}')

# Validate syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
