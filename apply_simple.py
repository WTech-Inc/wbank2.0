# Simple line-based approach - read lines, modify, write back
import py_compile

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line numbers for the functions/routes to remove
remove_ranges = []

# 1. Find trade_wcoins function
for i, line in enumerate(lines):
    if '@socketio.on("trade")' in line:
        start = i
        # Find the end - next decorator or blank line after the function
        for j in range(i+1, min(i+30, len(lines))):
            if lines[j].startswith('@socketio.on') and j > i+1:
                remove_ranges.append((start, j))
                break
            if lines[j].startswith('@app.route') and j > i+1:
                remove_ranges.append((start, j))
                break

    if '@socketio.on("friedBot")' in line:
        start = i
        for j in range(i+1, min(i+30, len(lines))):
            if lines[j].startswith('@socketio.on') and j > i+1:
                remove_ranges.append((start, j))
                break

    if '@socketio.on("tradeBot")' in line:
        start = i
        for j in range(i+1, min(i+30, len(lines))):
            if lines[j].startswith('@socketio.on') and j > i+1:
                remove_ranges.append((start, j))
                break
            if lines[j].startswith('@app.route') and j > i+1:
                remove_ranges.append((start, j))
                break

    if '@app.route("/wcoins/data")' in line:
        start = i
        for j in range(i+1, min(i+30, len(lines))):
            if lines[j].startswith('@app.route') and j > i+1:
                remove_ranges.append((start, j))
                break
            if lines[j].startswith('@socketio.on') and j > i+1:
                remove_ranges.append((start, j))
                break
            if lines[j].startswith('def ') and j > i+1:
                remove_ranges.append((start, j))
                break

# Remove from bottom to top to preserve line numbers
remove_ranges.sort(key=lambda x: x[0], reverse=True)
removed_count = 0
for start, end in remove_ranges:
    # Extend end to include blank lines after
    while end < len(lines) and lines[end].strip() == '':
        end += 1
    del lines[start:end]
    print(f'Removed lines {start+1}-{end}')
    removed_count += 1

print(f'\nRemoved {removed_count} blocks')

# Fix admin redirects
for i, line in enumerate(lines):
    if 'redirect("/admin/wbankkyc")' in line:
        lines[i] = line.replace('redirect("/admin/wbankkyc")', 'redirect("/admin/dashboard")')
        print(f'Fixed redirect at line {i+1}')
    if 'redirect("/admin/wbankwallet")' in line:
        lines[i] = line.replace('redirect("/admin/wbankwallet")', 'redirect("/admin/dashboard")')
        print(f'Fixed redirect at line {i+1}')

# Remove FLASK_ADMIN config
for i, line in enumerate(lines):
    if "FLASK_ADMIN_SWATCH" in line:
        lines[i] = ''
        print(f'Removed FLASK_ADMIN at line {i+1}')

# Remove Flask-Admin comment
for i, line in enumerate(lines):
    if line.strip() == '# 創建 Flask-Admin 管理界面':
        lines[i] = ''
        print(f'Removed Flask-Admin comment at line {i+1}')
    if line.strip() == '# 添加 SQLAlchemy 模型管理視圖':
        lines[i] = ''

# Fix restrict_routes for /admin
for i, line in enumerate(lines):
    if "if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/'):" in line:
        lines[i] = line.replace(
            "if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/'):",
            "if path == '/admin' or path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/'):"
        )
        print(f'Fixed restrict_routes at line {i+1}')

# Remove wangtry from users
for i, line in enumerate(lines):
    if 'wangtry' in line and 'generate_password_hash' in line:
        lines[i] = ''
        print(f'Removed wangtry from users at line {i+1}')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
