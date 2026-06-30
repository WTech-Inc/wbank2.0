import urllib.request, http.cookiejar, sys
from urllib.parse import urlencode

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Step 1: Login via /wbank/auth/v1/session (what the v1 login form submits to)
data = urlencode({'user': 'wangtry', 'pw': 'Chan1234#', 'url': '/wbank/client'}).encode()
r = opener.open('http://localhost:8080/wbank/auth/v1/session', data=data, timeout=5)
sys.stdout.write(f'Login POST: {r.status} -> {r.url}\n')

# Step 2: Try to access /wbank/client
r2 = opener.open('http://localhost:8080/wbank/client', timeout=5)
sys.stdout.write(f'Client page: {r2.status}, Size: {len(r2.read())}\n')

sys.stdout.flush()
