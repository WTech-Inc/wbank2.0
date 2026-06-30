import sys

path = 'E:\\wbank\\templates\\wbank\\home.html'

with open(path, 'rb') as f:
    raw = f.read()

sys.stdout.write(f'First 500 bytes hex:\n')
sys.stdout.write(raw[:500].hex(' ') + '\n')
sys.stdout.write(f'\nFirst 500 as latin-1:\n')
text = raw.decode('latin-1')
sys.stdout.write(text[:500] + '\n')

# Try: the file was originally UTF-8, read as latin-1, written as UTF-8
# So raw = utf8_encode(latin1_read(utf8_encode(original)))
# To fix: decode raw as utf-8, encode as latin-1, decode as utf-8
try:
    step1 = raw.decode('utf-8')  # Gets latin-1 characters as unicode
    step2 = step1.encode('latin-1')  # Converts back to original bytes
    original = step2.decode('utf-8')  # Finally correct UTF-8
    if '泓' in original or '財' in original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(original)
        sys.stdout.write(f'\nFIXED with utf8->latin1->utf8 approach\n')
        sys.stdout.write(f'First 200: {original[:200]}\n')
    else:
        sys.stdout.write(f'\nStill no Chinese after fix. Original bytes:\n')
        sys.stdout.write(raw[:500].hex(' ') + '\n')
except Exception as e:
    sys.stdout.write(f'\nError: {e}\n')

sys.stdout.flush()
