import sys
with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()
found = []
for keyword in ['log_audit', 'write_audit', 'startup', 'start_web', '# Startup']:
    pos = content.find(keyword)
    found.append(f'{keyword}: pos={pos}')
sys.stdout.write(str(found) + '\n')
sys.stdout.flush()
