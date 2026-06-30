import sys
with open('E:\\wbank\\run.log', 'rb') as f:
    data = f.read()

# Find ERROR markers
pattern = b'ERROR in app'
idx = data.find(pattern)
while idx >= 0:
    # Find end of error (next [ or end)
    end = data.find(b'\n[', idx)
    if end < 0:
        end = min(idx + 400, len(data))
    sys.stdout.buffer.write(data[idx:end] + b'\n---\n')
    idx = data.find(pattern, idx + 1)
sys.stdout.flush()
