"""Test swap page with proper session"""
import sys, ssl, urllib.request, urllib.parse, json
sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Login
data = urllib.parse.urlencode({"user": "wbank", "pw": "wbank@2026"}).encode()
req = urllib.request.Request("https://127.0.0.1:9001/admin/login", data=data, method="POST")
r = urllib.request.urlopen(req, context=ctx, timeout=5)
print(f"Login: {r.status}")

# Get cookies
cookies = r.headers.get_all("Set-Cookie") if hasattr(r.headers, "get_all") else []
print(f"Cookies: {cookies[:2] if cookies else 'None'}")

# Dashboard to establish session
r2 = urllib.request.urlopen("https://127.0.0.1:9001/admin/dashboard", context=ctx, timeout=5)
print(f"Dashboard: {r2.status}")

# Swap page
r3 = urllib.request.urlopen("https://127.0.0.1:9001/admin_swap", context=ctx, timeout=5)
html = r3.read().decode("utf-8", "replace")

print(f"Swap page: {len(html)} bytes")
print(f"Has btn-success: {'btn-success' in html}")
print(f"Has Approve: {'Approve' in html}")
print(f"Has Reject: {'Reject' in html}")
