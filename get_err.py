import sys
with open('E:\\wbank\\run.log', 'rb') as f:
    data = f.read()
# Find last 3000 bytes
sys.stdout.buffer.write(data[-3000:])
sys.stdout.flush()
