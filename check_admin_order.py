import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
lines = m.split('\n')

print('=== Admin route definitions ===')
for i, line in enumerate(lines):
    if '/admin' in line and ('@app.route' in line or 'def admin' in line):
        print(f'L{i+1}: {line.strip()[:120]}')
        for j in range(1, 4):
            if i+j < len(lines):
                l = lines[i+j].strip()
                if l:
                    print(f'  L{i+j+1}: {l[:120]}')
        print()

print('=== Catch-all route ===')
for i, line in enumerate(lines):
    if 'template_name' in line and '@app.route' in line:
        print(f'L{i+1}: {line.strip()}')
        for j in range(1, 5):
            if i+j < len(lines):
                print(f'  L{i+j+1}: {lines[i+j].strip()[:100]}')
        break
