"""Test private key endpoint"""
import urllib.request, json
from http.cookiejar import CookieJar
from urllib.parse import urlencode

base = 'http://localhost:9002'
cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Login
data = urlencode({'pw': 'wbank@2026', 'u': 'wangtry'}).encode()
req = urllib.request.Request(f'{base}/admin/login', data=data,
    headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded'})
r = opener.open(req, timeout=10)
print(f'Login: {r.status}')

# Get private key
req2 = urllib.request.Request(f'{base}/wbank/settings/private_key',
    headers={'User-Agent': 'Mozilla/5.0'})
r2 = opener.open(req2, timeout=10)
d = json.loads(r2.read())
print(f'Private key endpoint: {r2.status}')
print(f'Address: {d.get("address", "N/A")}')
print(f'Has private_key: {bool(d.get("private_key"))}')
if d.get('private_key'):
    print(f'PK starts with: {d["private_key"][:20]}...')
else:
    print('ERROR: private_key is None/empty')
