import sys, glob

for f in glob.glob('E:\\wbank\\templates\\**\\*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            fh.read()
    except UnicodeDecodeError as e:
        sys.stdout.write(f'CORRUPTED: {f} - {e}\n')
        # Try to fix by re-reading as latin1 and rewriting as utf-8
        try:
            with open(f, 'rb') as fh:
                data = fh.read()
            # Decode as latin1 (which never fails) and re-encode as utf-8
            text = data.decode('latin-1')
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(text)
            sys.stdout.write(f'  FIXED: Re-encoded as UTF-8\n')
        except Exception as e2:
            sys.stdout.write(f'  FAILED: {e2}\n')

for f in glob.glob('E:\\wbank\\templates\\*.html', recursive=False):
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            fh.read()
    except UnicodeDecodeError as e:
        sys.stdout.write(f'CORRUPTED: {f} - {e}\n')

sys.stdout.flush()
