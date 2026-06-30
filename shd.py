with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if line.strip().startswith('users = {'):
        for j in range(i, min(i+8, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
