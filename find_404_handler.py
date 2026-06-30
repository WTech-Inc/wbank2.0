import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
lines = m.split('\n')

# Find all error handlers and "disabled" references
for i, line in enumerate(lines):
    if 'disabled' in line.lower() or '404' in line or 'errorhandler' in line or 'abort' in line.lower() or 'Route' in line:
        print(f'L{i+1}: {line.strip()[:200]}')
        # Context
        if 'disabled' in line.lower() or 'errorhandler' in line:
            for j in range(1, 6):
                if i+j < len(lines):
                    print(f'  +{j}: {lines[i+j].strip()[:200]}')
            print()
