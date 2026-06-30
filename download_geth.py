"""Download Geth for Windows"""
import sys, os, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

path = 'E:\\wbank\\private-chain\\geth.exe'
os.makedirs('E:\\wbank\\private-chain', exist_ok=True)

urls = [
    'https://github.com/ethereum/go-ethereum/releases/download/v1.14.12/geth-windows-amd64-1.14.12-2b1d2e5c.exe',
    'https://gethstore.blob.core.windows.net/builds/geth-windows-amd64-1.14.12-2b1d2e5c.exe',
]

for url in urls:
    try:
        print(f'Downloading from GitHub...')
        urllib.request.urlretrieve(url, path)
        print(f'Geth downloaded to {path}')
        break
    except Exception as e:
        print(f'Failed: {str(e)[:80]}')
else:
    print('Could not download Geth automatically')
    print('Please download manually from:')
    print('https://github.com/ethereum/go-ethereum/releases/download/v1.14.12/geth-windows-amd64-1.14.12-2b1d2e5c.exe')
    print(f'Save to: {path}')
