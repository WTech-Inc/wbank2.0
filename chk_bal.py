import sys
with open('E:\\wbank\\run.log', 'rb') as f:
    data = f.read()
# Find the last ERROR
idx = data.rfind(b'ERROR in app')
if idx >= 0:
    end = data.find(b'\n127.0.0.1', idx)
    if end < 0:
        end = idx + 500
    sys.stdout.buffer.write(data[idx:end] + b'\n')
else:
    sys.stdout.buffer.write(b'No ERROR found in log\n')
sys.stdout.flush()
