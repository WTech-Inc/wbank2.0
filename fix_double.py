import sys

def fix_double_encoded_file(filepath):
    """Fix a file that was double-UTF8-encoded by latin-1 round-trip."""
    with open(filepath, 'rb') as f:
        raw = f.read()

    # Check if it's double-encoded by looking for sequences like \xc3\xa6\xc2\xb3\xc2\x93
    # (which is the UTF-8 encoding of \xe6\xb3\x93, the bytes for 泓)
    try:
        # First try: direct UTF-8 decode
        text = raw.decode('utf-8')
        # Check if it contains valid Chinese characters
        if '泓' in text or '財' in text or '銀' in text:
            sys.stdout.write(f'{filepath}: Already correctly encoded (has Chinese chars)\n')
            return False
    except:
        pass

    # The file might be double-encoded. Try decoding the raw bytes as latin-1 first
    # (which gives the original bytes), then interpret as UTF-8
    try:
        # If double-encoded: raw = utf8_encode(utf8_encode(chinese))
        # Step 1: decode as latin-1 to get the single-encoded bytes
        single_encoded = raw.decode('latin-1')
        # Step 2: encode back to bytes for step 3
        step2 = single_encoded.encode('latin-1')
        # Step 3: now these bytes should be valid single-UTF-8
        text = step2.decode('utf-8')

        # Verify it has Chinese
        if '泓' in text or '財' in text or '銀' in text:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            sys.stdout.write(f'{filepath}: FIXED (was double-encoded)\n')
            return True
        else:
            sys.stdout.write(f'{filepath}: No Chinese found after fix attempt\n')
            return False
    except Exception as e:
        sys.stdout.write(f'{filepath}: Error fixing: {e}\n')
        return False

files = [
    'E:\\wbank\\templates\\wbank.html',
    'E:\\wbank\\templates\\wbankClient.html',
    'E:\\wbank\\templates\\wbank\\home.html',
    'E:\\wbank\\templates\\wbank\\kyc.html',
    'E:\\wbank\\templates\\wbank\\createUser.html',
]

for f in files:
    fix_double_encoded_file(f)

sys.stdout.write('DONE\n')
sys.stdout.flush()
