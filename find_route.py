import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
lines = m.split('\n')

# Find all lines with "/auth/reg"
for i, line in enumerate(lines):
    if '/auth/reg' in line or 'Route disabled' in line:
        print(f'L{i+1}: {line.strip()[:200]}')
        # Also print a few lines after
        for j in range(1, 8):
            if i+j < len(lines):
                print(f'  +{j}: {lines[i+j].strip()[:200]}')
        print()
