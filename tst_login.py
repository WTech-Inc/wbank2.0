from urllib.request import Request, urlopen
from urllib.parse import urlencode

# Test login with password verification first
data = urlencode({'user':'wtech', 'pw':'wtechStaff1234#'}).encode()
req = Request('http://localhost:8080/admin/login', data=data, method='POST')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

try:
    r = urlopen(req, timeout=5)
    print(f'Status: {r.status}')
    print(f'URL: {r.url}')
    print(f'Headers: {dict(r.headers)}')
    body = r.read()
    print(f'Body ({len(body)} bytes): {body[:200]}')
except Exception as e:
    print(f'Error: {e}')
    if hasattr(e, 'code'):
        print(f'Code: {e.code}')
        print(f'Headers: {dict(e.headers)}')
