with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'run_https' in line or 'ssl_context' in line or 'use_debugger' in line or 'allow_unsafe' in line:
        print(f'{i+1}: {line.rstrip()}')
