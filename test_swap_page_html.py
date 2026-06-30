"""Test swap page HTML by logging in first"""
import sys, ssl, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Login first
data = urllib.parse.urlencode({"user": "wbank", "pw": "wbank@2026"}).encode()
req = urllib.request.Request("https://127.0.0.1:9001/admin/login", data=data, method="POST")
r = urllib.request.urlopen(req, context=ctx, timeout=5)

# Extract session cookie
cookies = r.headers.get_all("Set-Cookie")
session_cookie = None
for c in cookies or []:
    if "session=" in c:
        session_cookie = c.split(";")[0]
        break

# Request swap page with cookie
if session_cookie:
    req2 = urllib.request.Request("https://127.0.0.1:9001/admin/swap", headers={"Cookie": session_cookie})
    r2 = urllib.request.urlopen(req2, context=ctx, timeout=5)
    html = r2.read().decode("utf-8", "replace")
    # Find the onclick JS
    idx = html.find("doApprove")
    if idx >= 0:
        print("doApprove found:", repr(html[idx-30:idx+80]))
    else:
        print("doApprove NOT FOUND in HTML")
        print("Page size:", len(html))
        # Look for any onclick
        idx2 = html.find("onclick")
        if idx2 >= 0:
            print("onclick found:", repr(html[idx2:idx2+100]))
        else:
            print("No onclick found in page")
else:
    print("No session cookie from login")
