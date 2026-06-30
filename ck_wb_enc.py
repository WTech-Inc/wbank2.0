import hashlib, requests, sys

# Get the real page
ak = hashlib.sha256('wtech->wtech888->true'.encode()).hexdigest()
url = f'http://localhost:8080/wbank/home?accessKey={ak}'
r = requests.get(url, timeout=5)
sys.stdout.write(f'Status: {r.status_code}\n')
sys.stdout.write(f'Content-Type: {r.headers.get("Content-Type")}\n')
sys.stdout.write(f'Encoding: {r.encoding}\n')
sys.stdout.write(f'Size: {len(r.text)}\n')
sys.stdout.write(f'First 500 chars: {r.text[:500]}\n')
sys.stdout.write(f'Apparent encoding: {r.apparent_encoding}\n')
sys.stdout.flush()
