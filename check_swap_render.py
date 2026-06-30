"""Check rendered swap page HTML"""
import sys, ssl, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Login as admin
data = urllib.parse.urlencode({"user": "wbank", "pw": "wbank@2026"}).encode()
req = urllib.request.Request("https://127.0.0.1:9001/admin/login", data=data, method="POST")
r = urllib.request.urlopen(req, context=ctx, timeout=5)

# Follow redirect to dashboard (to establish session)
r2 = urllib.request.urlopen("https://127.0.0.1:9001/admin/dashboard", context=ctx, timeout=5)

# Now get swap page
r3 = urllib.request.urlopen("https://127.0.0.1:9001/admin/swap", context=ctx, timeout=5)
html = r3.read().decode("utf-8", "replace")

print(f"Page size: {len(html)} bytes")
print(f"Has btn-success: {'btn-success' in html}")
print(f"Has Approve button: {'Approve</button>' in html}")
print(f"Has onclick: {'onclick' in html}")

# Show what's in the Action section
idx = html.find("Action</th>")
if idx >= 0:
    print(f"After Action header: {html[idx:idx+500]}")
else:
    print("Action header not found!")
    # Show table structure
    tidx = html.find("<table")
    if tidx >= 0:
        print(f"Table starts: {html[tidx:tidx+300]}")
