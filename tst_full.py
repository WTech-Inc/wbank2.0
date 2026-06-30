import urllib.request, http.cookiejar, json, sys

# Create cookie jar and opener
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Step 1: Try login
from urllib.parse import urlencode
data = urlencode({'user': 'wtech', 'pw': 'wtechStaff1234#'}).encode()
sys.stdout.write('Step 1: POST /admin/login\n')
r = opener.open('http://localhost:8080/admin/login', data=data, timeout=5)
sys.stdout.write(f'  Status: {r.status}, URL: {r.url}\n')

# Step 2: Access dashboard with cookie
sys.stdout.write('Step 2: GET /admin/dashboard\n')
r2 = opener.open('http://localhost:8080/admin/dashboard', timeout=5)
sys.stdout.write(f'  Status: {r2.status}, URL: {r2.url}, Size: {len(r2.read())}\n')

# Step 3: Try stats API
sys.stdout.write('Step 3: GET /admin/api/stats\n')
r3 = opener.open('http://localhost:8080/admin/api/stats', timeout=5)
data3 = json.loads(r3.read())
sys.stdout.write(f'  Status: {r3.status}, Data: {json.dumps(data3, ensure_ascii=False)}\n')

# Step 4: Try users API
sys.stdout.write('Step 4: GET /admin/api/users\n')
r4 = opener.open('http://localhost:8080/admin/api/users', timeout=5)
data4 = json.loads(r4.read())
sys.stdout.write(f'  Status: {r4.status}, Users count: {len(data4)}\n')

sys.stdout.flush()
