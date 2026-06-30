"""Test admin login and check session"""
import sys, ssl, urllib.request, urllib.parse, json
sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Login as admin
data = urllib.parse.urlencode({"user": "wbank", "pw": "wbank@2026"}).encode()
req = urllib.request.Request("https://127.0.0.1:9001/admin/login", data=data, method="POST")
try:
    r = urllib.request.urlopen(req, context=ctx, timeout=5)
    print(f"Login: {r.status}")
    cookies = r.headers.get_all("Set-Cookie") if hasattr(r.headers, 'get_all') else []
    if cookies:
        print(f"Cookies: {[c[:60] for c in cookies]}")
    else:
        print("No cookies in response")
        # Check redirect
        if r.status == 302:
            print(f"Redirect to: {r.headers.get('Location')}")
            # Follow redirect for dashboard
            r2 = urllib.request.urlopen(r.headers.get('Location'), context=ctx, timeout=5)
            print(f"Dashboard: {r2.status} ({len(r2.read())} bytes)")
    # Test stats API
    r3 = urllib.request.urlopen("https://127.0.0.1:9001/admin/api/stats", context=ctx, timeout=5)
    print(f"Stats API: {r3.status} {r3.read().decode()[:100]}")
except urllib.error.HTTPError as e:
    print(f"Error: {e.code} - {e.read().decode()[:200]}")
except Exception as e:
    print(f"Exception: {e}")
