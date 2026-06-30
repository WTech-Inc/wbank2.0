with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2485, 2510):
    if i < len(lines):
        print(f'{i+1}: {lines[i].rstrip()}')
