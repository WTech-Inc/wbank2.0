with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'def wbank_v1_auth_login():' in line:
        for j in range(i-2, min(i+10, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
