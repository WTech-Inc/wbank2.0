"""Download Geth - correct URL"""
import sys, os, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://gethstore.blob.core.windows.net/builds/geth-windows-amd64-1.17.3-117e067f.exe'
dest = 'E:\\wbank\\private-chain\\geth.exe'

print('Downloading Geth...')
urllib.request.urlretrieve(url, dest)
size = os.path.getsize(dest)
print(f'OK: {size/1024/1024:.0f} MB downloaded')

# Check version
import subprocess
result = subprocess.run([dest, 'version'], capture_output=True, text=True, timeout=10)
print('Version:', result.stdout[:100])
