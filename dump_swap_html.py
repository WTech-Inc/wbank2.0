"""Dump rendered swap page HTML for debugging"""
import sys, ssl, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Login
data = urllib.parse.urlencode({"user": "wbank", "pw": "wbank@2026"}).encode()
req = urllib.request.Request("https://127.0.0.1:9001/admin/login", data=data, method="POST")
r = urllib.request.urlopen(req, context=ctx, timeout=5)

# Dashboard to set session
r2 = urllib.request.urlopen("https://127.0.0.1:9001/admin/dashboard", context=ctx, timeout=5)

# Swap page
r3 = urllib.request.urlopen("https://127.0.0.1:9001/admin/swap", context=ctx, timeout=5)
html = r3.read().decode("utf-8", "replace")

print("=== FULL HTML ===")
print(html)
