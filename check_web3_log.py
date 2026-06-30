import sys
sys.stdout.reconfigure(encoding='utf-8')

log = open('E:\\wbank\\run.log', 'rb').read().decode('utf-8', 'replace')
lines = log.split('\n')
# Find all Traceback errors
for i, line in enumerate(lines):
    if 'Traceback' in line or 'Error' in line:
        start = max(0, i-1)
        end = min(len(lines), i+15)
        for j in range(start, end):
            print(f'{j}: {lines[j][:200]}')
        print('---')
