import sys
with open('E:\\wbank\\run.log', 'rb') as f:
    data = f.read()
# Find last ERROR in app
idx = data.rfind(b'ERROR in app')
if idx >= 0:
    end = data.find(b'\n127.0.0.1', idx)
    if end < 0:
        end = min(idx + 800, len(data))
    # Extract the useful part
    block = data[idx:end]
    # Find the actual error message
    err_idx = block.rfind(b'Error:')
    if err_idx >= 0:
        sys.stdout.buffer.write(b'Error: ' + block[err_idx:err_idx+200])
    else:
        # Show last line
        lines = block.split(b'\n')
        for line in lines[-5:]:
            sys.stdout.buffer.write(line + b'\n')
else:
    sys.stdout.buffer.write(b'No ERROR in log\n')
    # Check if there's a different type of error
    idx2 = data.rfind(b'Traceback')
    if idx2 >= 0:
        sys.stdout.buffer.write(data[idx2:idx2+300] + b'\n')
    else:
        # Check startup
        sys.stdout.buffer.write(data[-500:] + b'\n')
sys.stdout.flush()
