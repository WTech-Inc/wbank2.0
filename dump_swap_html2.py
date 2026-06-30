"""Debug swap page - check redirect chain"""
import sys, ssl, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Login without auto-redirect
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirect)
opener.ctx = ctx

def open_with_ctx(url, data=None):
    req = urllib.request.Request(url, data=data)
    return opener.open(req, timeout=5)

# Try login
data = urllib.parse.urlencode({"user": "wbank", "pw": "wbank@2026"}).encode()
r = open_with_ctx("https://127.0.0.1:9001/admin/login", data)
print(f"Login: {r.status} -> {r.headers.get('Location','')}")
print(f"Cookies: {r.headers.get_all('Set-Cookie') if hasattr(r.headers,'get_all') else 'none'}")

# Try swap page directly
r2 = open_with_ctx("https://127.0.0.1:9001/admin/swap")
print(f"Swap: {r2.status} -> {r2.headers.get('Location','')}")
body = r2.read().decode("utf-8", "replace")
if "Swap Admin" in body:
    print("SWAP PAGE LOADED SUCCESSFULLY!")
    print(f"Has buttons: {'btn-success' in body}")
    print(f"Has onclick: {'onclick' in body}")
elif "login-screen" in body:
    print("Redirected to login page (not authenticated)")
else:
    print(f"Unknown response, first 200 chars: {body[:200]}")
