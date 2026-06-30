with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line with 'user_ip = request.remote_addr' after '/wbank' route
target_func = False
for i, line in enumerate(lines):
    if 'def wbank():' in line:
        target_func = True
    if target_func and 'user_ip = request.remote_addr' in line:
        # Insert local IP check after this line
        insert_text = '''
    # Handle local/private IPs
    if user_ip in ('127.0.0.1', '::1', 'localhost') or user_ip.startswith(('192.168.', '10.', '172.16.')):
      return render_template("wbank.html", site_key=CF_SITES_KEY)
'''
        lines.insert(i+2, insert_text)
        print(f'Inserted local IP check at line {i+2}')
        break

# Also change the abort(502) to render_template on the exception and fail cases
for i, line in enumerate(lines):
    if 'return abort(502)' in line and target_func:
        lines[i] = line.replace('return abort(502)', 'return render_template("wbank.html", site_key=CF_SITES_KEY)')
        print(f'Changed line {i+1} from abort to render_template')
    if 'def wbank_transfer():' in line:
        target_func = False

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
