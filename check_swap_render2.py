"""Check rendered HTML content"""
import sys, ssl, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

data = urllib.parse.urlencode({"user": "wbank", "pw": "wbank@2026"}).encode()
req = urllib.request.Request("https://127.0.0.1:9001/admin/login", data=data, method="POST")
r = urllib.request.urlopen(req, context=ctx, timeout=5)
r2 = urllib.request.urlopen("https://127.0.0.1:9001/admin/dashboard", context=ctx, timeout=5)
r3 = urllib.request.urlopen("https://127.0.0.1:9001/admin/swap", context=ctx, timeout=5)
html = r3.read().decode("utf-8", "replace")

# Find what's between script tags
import re
scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
print(f"Script blocks: {len(scripts)}")
for i, s in enumerate(scripts):
    print(f"\nScript {i+1}: {len(s)} chars")
    if "btn-success" in s:
        print("  HAS btn-success in script!")
    if "Approve" in s:
        print("  HAS Approve in script!")
        idx = s.find("Approve")
        print(f"  Context: {s[idx-30:idx+60]}")
