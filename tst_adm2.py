import urllib.request, http.cookiejar, json, sys
from urllib.parse import urlencode

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Login as wangtry from database
data = urlencode({'user': 'wangtry', 'pw': 'Chan1234#'}).encode()
sys.stdout.write('Step 1: POST /admin/login (wangtry/Chan1234#)\n')
r = opener.open('http://localhost:8080/admin/login', data=data, timeout=5)
sys.stdout.write(f'  Status: {r.status}, URL: {r.url}\n')

sys.stdout.write('Step 2: GET /admin/dashboard\n')
r2 = opener.open('http://localhost:8080/admin/dashboard', timeout=5)
sys.stdout.write(f'  Status: {r2.status}, URL: {r2.url}, Size: {len(r2.read())}\n')

sys.stdout.write('Step 3: GET /admin/api/stats\n')
r3 = opener.open('http://localhost:8080/admin/api/stats', timeout=5)
data3 = json.loads(r3.read())
sys.stdout.write(f'  Status: {r3.status}, Data: {json.dumps(data3, ensure_ascii=False)}\n')

sys.stdout.write('Step 4: GET /admin/api/users\n')
r4 = opener.open('http://localhost:8080/admin/api/users', timeout=5)
data4 = json.loads(r4.read())
sys.stdout.write(f'  Status: {r4.status}, Users: {len(data4)}\n')

sys.stdout.write('Step 5: GET /admin/api/export/audit_json\n')
r5 = opener.open('http://localhost:8080/admin/api/export/audit_json', timeout=5)
data5 = json.loads(r5.read())
sys.stdout.write(f'  Status: {r5.status}, Entries: {len(data5)}\n')

sys.stdout.write('Step 6: GET /wbank\n')
r6 = urllib.request.urlopen('http://localhost:8080/wbank', timeout=5)
sys.stdout.write(f'  Status: {r6.status}, Size: {len(r6.read())}\n')

sys.stdout.flush()
