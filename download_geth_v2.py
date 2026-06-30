"""Download Geth alltools zip for Windows"""
import sys, os, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

dest = 'E:\\wbank\\private-chain\\geth-alltools.zip'

urls = [
    'https://github.com/ethereum/go-ethereum/releases/download/v1.14.12/geth-alltools-windows-amd64-1.14.12-2b1d2e5c.zip',
    'https://github.com/ethereum/go-ethereum/releases/download/v1.14.11/geth-alltools-windows-amd64-1.14.11-2b1d2e5c.zip',
    'https://github.com/ethereum/go-ethereum/releases/download/v1.14.10/geth-alltools-windows-amd64-1.14.10-2b1d2e5c.zip',
    'https://github.com/ethereum/go-ethereum/releases/download/v1.14.9/geth-alltools-windows-amd64-1.14.9-2b1d2e5c.zip',
]

for url in urls:
    name = url.split('/')[-1]
    print(f'Trying: {name}')
    try:
        urllib.request.urlretrieve(url, dest)
        size = os.path.getsize(dest)
        if size > 10000000:
            print(f'OK! {size/1024/1024:.0f} MB downloaded')
            # Extract geth.exe
            import zipfile
            with zipfile.ZipFile(dest, 'r') as z:
                for f in z.namelist():
                    if f.endswith('geth.exe'):
                        print(f'Extracting: {f}')
                        z.extract(f, 'E:\\wbank\\private-chain\\')
                        # Move the exe to the root
                        import shutil
                        src = os.path.join('E:\\wbank\\private-chain', f)
                        dst = 'E:\\wbank\\private-chain\\geth.exe'
                        if src != dst and os.path.exists(src):
                            os.rename(src, dst)
                        print('Geth ready!')
                        break
            break
        else:
            print(f'Too small: {size}')
            os.remove(dest)
    except Exception as e:
        print(f'Failed: {str(e)[:80]}')
        if os.path.exists(dest):
            os.remove(dest)
else:
    print('\nCould not download Geth automatically.')
    print('Please download manually:')
    print('1. Go to: https://geth.ethereum.org/downloads/')
    print('2. Download "Geth & Tools" for Windows')
    print(f'3. Extract geth.exe to: E:\\wbank\\private-chain\\geth.exe')
