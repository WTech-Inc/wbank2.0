import urllib.request, http.cookiejar, json, sys
from urllib.parse import urlencode

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Login first
data = urlencode({'user': 'wangtry', 'pw': 'Chan1234#'}).encode()
r = opener.open('http://localhost:8080/admin/login', data=data, timeout=5)
sys.stdout.write(f'Login: {r.status} -> {r.url}\n')

# Test verify_user POST
req = urllib.request.Request(
    'http://localhost:8080/admin/api/verify_user',
    data=json.dumps({'username': 'wbank'}).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST')
r2 = opener.open(req, timeout=5)
sys.stdout.write(f'Verify wbank: {r2.status} -> {r2.read().decode()}\n')

# Test freeze_user POST
req3 = urllib.request.Request(
    'http://localhost:8080/admin/api/freeze_user',
    data=json.dumps({'username': 'wbank'}).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST')
r3 = opener.open(req3, timeout=5)
sys.stdout.write(f'Freeze wbank: {r3.status} -> {r3.read().decode()}\n')

# Test update_balance POST
req4 = urllib.request.Request(
    'http://localhost:8080/admin/api/update_balance',
    data=json.dumps({'username': 'wbank', 'amount': 100}).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST')
r4 = opener.open(req4, timeout=5)
sys.stdout.write(f'Balance wbank: {r4.status} -> {r4.read().decode()}\n')

sys.stdout.write('All POST APIs work!\n')
sys.stdout.flush()
