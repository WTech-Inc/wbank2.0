with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find admin_login function
for i, line in enumerate(lines):
    if 'def admin_login():' in line and 'admin_login_page' not in line:
        # Print surrounding lines with context
        start = max(0, i-2)
        end = min(len(lines), i+20)
        for j in range(start, end):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
