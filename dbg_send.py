import urllib.request, http.cookiejar, json, sys
from urllib.parse import urlencode

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
data = urlencode({'user': 'wangtry', 'pw': 'Chan1234#', 'url': '/wbank/client'}).encode()
opener.open('http://localhost:8080/wbank/auth/v1/session', data=data, timeout=5)

# Send WTC - with debug
req = urllib.request.Request(
    'http://localhost:8080/wbank/web3/send',
    data=json.dumps({'to': '0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18', 'amount': 100}).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST')
try:
    r = opener.open(req, timeout=10)
    sys.stdout.write(f'Send status: {r.status}\n')
    sys.stdout.write(f'Send body: {r.read().decode()}\n')
except urllib.request.HTTPError as e:
    sys.stdout.write(f'Send error {e.code}: {e.read().decode()[:300]}\n')

# Also test the info endpoint while we're at it
r2 = opener.open('http://localhost:8080/wbank/web3/info', timeout=5)
sys.stdout.write(f'Info: {r2.status} - balance: {json.loads(r2.read())["balance"]}\n')
sys.stdout.flush()
