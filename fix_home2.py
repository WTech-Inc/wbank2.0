import sys

path = 'E:\\wbank\\templates\\wbank\\home.html'

with open(path, 'rb') as f:
    raw = f.read()

# Fix: decode raw as utf-8, encode as latin-1, decode as utf-8
try:
    step1 = raw.decode('utf-8')
    step2 = step1.encode('latin-1')
    original = step2.decode('utf-8')
except Exception as e:
    # If it fails, the file might not be double-encoded
    sys.stdout.buffer.write(f'Fix failed: {e}\n'.encode('utf-8'))
    sys.exit(1)

# Write fixed content
with open(path, 'w', encoding='utf-8') as f:
    f.write(original)

# Verify
with open(path, 'rb') as f:
    verify = f.read()

if '泓'.encode('utf-8') in verify or '財'.encode('utf-8') in verify:
    sys.stdout.buffer.write(f'FIXED: Has Chinese characters now\n'.encode('utf-8'))
    # Show the title
    title_start = verify.find(b'<title>')
    title_end = verify.find(b'</title>', title_start)
    if title_start >= 0:
        sys.stdout.buffer.write(f'Title: {verify[title_start:title_end+8]}\n'.encode('utf-8'))
else:
    sys.stdout.buffer.write(f'Still no Chinese characters\n'.encode('utf-8'))
    sys.stdout.buffer.write(f'Bytes around 100: {verify[90:200].hex(" ")}\n'.encode('utf-8'))

sys.stdout.flush()
