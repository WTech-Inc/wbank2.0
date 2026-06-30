import sys
sys.stdout.reconfigure(encoding='utf-8')

log = open('E:\\wbank\\run.log', 'rb').read().decode('utf-8', 'replace')
lines = log.split('\n')
# Find "Failed to save" or "WARN" lines
for line in lines:
    if 'Failed to save' in line or 'WARN' in line or 'Traceback' in line or 'Error' in line:
        print(line[:200])
