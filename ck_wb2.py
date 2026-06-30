with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
# Full /wbank route from line 1660
for i in range(1660, 1690):
    if i < len(lines):
        print(f'{i+1}: {lines[i].rstrip()}')
