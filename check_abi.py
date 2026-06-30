lines = open('E:\\wbank\\wbank_web3.py', 'rb').read().split(b'\n')
for i, line in enumerate(lines):
    if b'WTC_ABI' in line or b'false' in line or b'true' in line:
        if b'import' not in line and b'False' not in line and b'True' not in line:
            print(f'Line {i+1}: {line.decode("utf-8", errors="replace")[:200]}')
