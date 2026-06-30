with open('E:\\wbank\\templates\\wbank\\login.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'input' in line or 'form' in line:
        if 'action' in line or 'name' in line or 'type' in line or 'hidden' in line:
            print(f'{i+1}: {line.rstrip()[:120]}')
