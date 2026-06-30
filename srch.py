import sys
with open('E:\\wbank\\main.py', 'rb') as f:
    content = f.read()
# Search for audit-related text
for keyword in [b'audit', b'log_audit', b'handle_transfer']:
    pos = content.find(keyword)
    sys.stdout.write(f'{keyword.decode()}: pos={pos}\n')
    if pos >= 0:
        sys.stdout.write(f'  context: {content[pos:pos+100]}\n')
sys.stdout.flush()
