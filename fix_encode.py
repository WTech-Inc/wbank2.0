import glob, sys

# Check ALL project files for encoding issues
for pattern in ['E:\\wbank\\templates\\**\\*.html', 'E:\\wbank\\templates\\*.html']:
    for f in glob.glob(pattern, recursive=True):
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                fh.read()
        except UnicodeDecodeError:
            try:
                with open(f, 'rb') as fh:
                    data = fh.read()
                # Try to decode with various encodings
                for enc in ['big5', 'gbk', 'gb2312', 'latin-1']:
                    try:
                        text = data.decode(enc)
                        with open(f, 'w', encoding='utf-8') as fh:
                            fh.write(text)
                        sys.stdout.write(f'FIXED: {f} (was {enc})\n')
                        break
                    except:
                        continue
                else:
                    # Last resort: decode as latin1 (never fails)
                    text = data.decode('latin-1')
                    with open(f, 'w', encoding='utf-8') as fh:
                        fh.write(text)
                    sys.stdout.write(f'FIXED: {f} (as latin-1)\n')
            except Exception as e:
                sys.stdout.write(f'FAILED: {f} - {e}\n')

# Also check main .py files
for f in glob.glob('E:\\wbank\\*.py'):
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            fh.read()
    except UnicodeDecodeError:
        try:
            with open(f, 'rb') as fh:
                data = fh.read()
            text = data.decode('latin-1')
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(text)
            sys.stdout.write(f'FIXED: {f} (as latin-1)\n')
        except Exception as e:
            sys.stdout.write(f'FAILED: {f} - {e}\n')

sys.stdout.write('DONE\n')
sys.stdout.flush()
