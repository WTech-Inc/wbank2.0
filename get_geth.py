"""Download Geth for Windows - try multiple sources"""
import sys, os, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

dest = 'E:\\wbank\\private-chain\\geth.exe'
os.makedirs('E:\\wbank\\private-chain', exist_ok=True)

urls = [
    # Official Geth releases
    'https://github.com/ethereum/go-ethereum/releases/download/v1.14.13/geth-windows-amd64-1.14.13-2b1d2e5c.exe',
    'https://github.com/ethereum/go-ethereum/releases/download/v1.14.12/geth-windows-amd64-1.14.12-2b1d2e5c.exe',
    'https://github.com/ethereum/go-ethereum/releases/download/v1.14.11/geth-windows-amd64-1.14.11-2b1d2e5c.exe',
    'https://github.com/ethereum/go-ethereum/releases/download/v1.14.10/geth-windows-amd64-1.14.10-2b1d2e5c.exe',
    # Geth store
    'https://gethstore.blob.core.windows.net/builds/geth-windows-amd64-1.14.13-2b1d2e5c.exe',
    'https://gethstore.blob.core.windows.net/builds/geth-windows-amd64-1.14.12-2b1d2e5c.exe',
]

downloaded = False
for url in urls:
    try:
        print(f'Trying: {url.split("/")[-1]}')
        urllib.request.urlretrieve(url, dest)
        size = os.path.getsize(dest)
        if size > 1000000:  # > 1MB means it's real
            print(f'OK! {size/1024/1024:.0f} MB')
            downloaded = True
            break
        else:
            print(f'Too small: {size} bytes')
    except Exception as e:
        print(f'Failed: {str(e)[:60]}')

if not downloaded:
    print('\nCould not download automatically.')
    print('Please download manually:')
    print('1. Go to: https://geth.ethereum.org/downloads/')
    print('2. Click "Geth for Windows"')
    print(f'3. Extract geth.exe to: {dest}')
