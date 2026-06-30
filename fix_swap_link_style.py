"""Make swap link use CSS class like other sidebar links"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8").read()

old = '<a href="/admin/swap" style="color:#bdc3c7;text-decoration:none;display:block;padding:12px 25px;">SWAP</a>'
new = '    <a href="/admin/swap">SWAP</a>'

if old in c:
    c = c.replace(old, new)
    open("E:/wbank/templates/admin/index.html", "w", encoding="utf-8").write(c)
    print("OK")
else:
    print("Pattern not found!")
