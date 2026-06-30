with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

capture = False
for i, line in enumerate(lines):
    if 'def start_web():' in line:
        capture = True
    if capture:
        print(f'{i+1}: {line.rstrip()}')
        if capture and i > 3430:
            break
