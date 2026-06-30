with open('E:\\wbank\\main.py', 'rb') as f:
    lines = f.readlines()
for i in range(200, 210):
    if i < len(lines):
        print(f'{i+1}: {lines[i]}')
