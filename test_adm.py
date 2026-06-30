import urllib.request, json

# Test login redirect
from urllib.parse import urlencode
data = urlencode({'user':'wtech', 'pw':'wtechStaff1234#'}).encode()
req = urllib.request.Request('http://localhost:8080/admin/login', data=data, method='POST')
try:
    r = urllib.request.urlopen(req, timeout=5)
    print(f'Login: {r.status} -> {r.url}')
    cookies = r.headers.get_all('Set-Cookie')
    print(f'Cookies: {cookies}')
except Exception as e:
    print(f'Login error: {e}')

# Test dashboard with cookie (simulate logged-in)
print()
print('=== Testing API endpoints ===')
for p in ['/admin/api/stats', '/admin/api/users']:
    try:
        r = urllib.request.urlopen('http://localhost:8080' + p, timeout=5)
        data = json.loads(r.read())
        print(f'{p}: {r.status} - {json.dumps(data, ensure_ascii=False)[:200]}')
    except Exception as e:
        print(f'{p}: Error - {e}')
