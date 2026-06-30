import urllib.request, http.cookiejar, json, sys
from urllib.parse import urlencode

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
data = urlencode({'user': 'wangtry', 'pw': 'Chan1234#', 'url': '/wbank/client'}).encode()
opener.open('http://localhost:8080/wbank/auth/v1/session', data=data, timeout=5)

# Send WTC
req = urllib.request.Request(
    'http://localhost:8080/wbank/web3/send',
    data=json.dumps({'to': '0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18', 'amount': 100}).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST')
r = opener.open(req, timeout=10)
sys.stdout.write(f'Send: {r.status}\n')
sys.stdout.write(f'Result: {json.dumps(json.loads(r.read()), indent=2)}\n')

# Check balance
r2 = opener.open('http://localhost:8080/wbank/web3/info', timeout=5)
sys.stdout.write(f'New balance: {json.loads(r2.read())["balance"]}\n')

# Check history
r3 = opener.open('http://localhost:8080/wbank/web3/history', timeout=5)
sys.stdout.write(f'History: {json.loads(r3.read())}\n')
sys.stdout.flush()
