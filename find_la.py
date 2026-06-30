with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('def log_audit(')
if idx >= 0:
    # Show 30 lines from the function
    lines = content[idx:].split('\n')
    for i, line in enumerate(lines[:15]):
        print(f'{i}: {line}')
