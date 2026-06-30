import urllib.request, http.cookiejar, json, sys
from urllib.parse import urlencode

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Login V1
data = urlencode({'user': 'wangtry', 'pw': 'Chan1234#', 'url': '/wbank/client'}).encode()
r = opener.open('http://localhost:8080/wbank/auth/v1/session', data=data, timeout=5)
sys.stdout.write(f'Login: {r.status} -> {r.url}\n')

# Try web3 info
r2 = opener.open('http://localhost:8080/wbank/web3/info', timeout=5)
sys.stdout.write(f'Web3 info: {r2.status}\n')
sys.stdout.write(f'Body: {r2.read().decode()[:500]}\n')
sys.stdout.flush()
