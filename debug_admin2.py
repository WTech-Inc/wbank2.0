"""Debug admin login - check redirect chain"""
import sys, ssl, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Don't auto-follow redirects
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirect)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

data = urllib.parse.urlencode({"user": "wbank", "pw": "wbank@2026"}).encode()
req = urllib.request.Request("https://127.0.0.1:9001/admin/login", data=data, method="POST")

try:
    r = opener.open(req, timeout=5)
    print(f"Status: {r.status}")
    print(f"Location: {r.headers.get('Location')}")
    print(f"Headers: {dict(r.headers)}")
    print(f"Body: {r.read().decode('utf-8','replace')[:200]}")
except urllib.error.HTTPError as e:
    print(f"Error: {e.code}")
    print(f"Body: {e.read().decode('utf-8','replace')[:200]}")
