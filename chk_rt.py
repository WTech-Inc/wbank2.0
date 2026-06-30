with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    s = line.strip()
    if '/admin' in s and ('@app.route' in s or 'ALLOWED' in s or 'startswith' in s):
        print(f'{i}: {s}')
