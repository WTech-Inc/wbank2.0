import urllib.request, http.cookiejar, json, sys
from urllib.parse import urlencode

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Login
data = urlencode({'user': 'wangtry', 'pw': 'Chan1234#'}).encode()
opener.open('http://localhost:8080/admin/login', data=data, timeout=5)

# Get wbank balance first
users = json.loads(opener.open('http://localhost:8080/admin/api/users', timeout=5).read())
for u in users:
    if u['username'] == 'wbank':
        sys.stdout.write(f'wbank balance before: {u["balance"]}\n')

# Test update_balance
req = urllib.request.Request(
    'http://localhost:8080/admin/api/update_balance',
    data=json.dumps({'username': 'wbank', 'amount': 100}).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST')
try:
    r = opener.open(req, timeout=5)
    sys.stdout.write(f'Status: {r.status}\n')
    sys.stdout.write(f'Body: {r.read().decode()}\n')
except urllib.request.HTTPError as e:
    sys.stdout.write(f'Error {e.code}: {e.read().decode()[:500]}\n')

sys.stdout.flush()
