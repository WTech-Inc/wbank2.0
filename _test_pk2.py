"""Test private key with user login"""
import urllib.request, json
from http.cookiejar import CookieJar

base = 'http://localhost:9002'
cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Login as user via /wbank/auth/v1/login
data = b'username=wangtry&password=123'
req = urllib.request.Request(base+'/wbank/auth/v1/login', data=data,
    headers={'User-Agent':'Mozilla/5.0','Content-Type':'application/x-www-form-urlencoded'})
try:
    r = opener.open(req, timeout=10)
    print('Login status:', r.status, 'url:', r.url)
except Exception as e:
    print(f'Login error: {e}')

# Try private key
req2 = urllib.request.Request(base+'/wbank/settings/private_key',
    headers={'User-Agent':'Mozilla/5.0'})
try:
    r2 = opener.open(req2, timeout=10)
    d = json.loads(r2.read())
    print('PK endpoint:', r2.status)
    print('Has PK:', bool(d.get('private_key')))
    if d.get('private_key'):
        print('PK starts:', d['private_key'][:30])
    print('Address:', d.get('address'))
except Exception as e:
    print(f'PK error: {e}')
    # Try to read the error body
    if hasattr(e, 'read'):
        print('Body:', e.read()[:200])
