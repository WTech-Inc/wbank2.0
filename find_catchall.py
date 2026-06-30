import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
lines = m.split('\n')

for i, line in enumerate(lines):
    if 'wbank_wtech_find_page' in line or 'template_name' in line and 'route' in line.lower():
        print(f'L{i+1}: {line.strip()[:200]}')
        for j in range(1, 30):
            if i+j < len(lines):
                l = lines[i+j].strip()
                if l:
                    print(f'  L{i+j+1}: {l[:200]}')
        print('---')
        break

# Also check for any remaining "Route disabled"
print('=== Checking for "Route disabled" ===')
for i, line in enumerate(lines):
    if 'Route disabled' in line or 'route_disabled' in line:
        print(f'FOUND L{i+1}: {line.strip()[:200]}')
        # print context
        for j in range(-2, 10):
            if i+j >= 0 and i+j < len(lines):
                print(f'  {lines[i+j].strip()[:200]}')
        print()

print('=== Checking for /auth handling ===')
for i, line in enumerate(lines):
    if '/auth' in line and 'route' in line.lower():
        print(f'L{i+1}: {line.strip()[:200]}')
