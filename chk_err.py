import sys
with open('E:\\wbank\\run.log', 'r', encoding='utf-8') as f:
    content = f.read()
# Find error sections
idx = content.find('ERROR in app')
while idx >= 0:
    end = content.find('\n[', idx + 1)
    if end < 0:
        end = idx + 500
    sys.stdout.write(content[idx:end] + '\n---\n')
    idx = content.find('ERROR in app', end)
sys.stdout.flush()
