"""Add ONE simple hyperlink to swap page - zero JS changes"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8").read()

# Very precise: find the KYC link closing </a> and add swap link after it
target = '</a>\n    <hr style="border-color: #34495e;">'
swap_link = '</a>\n        <a href="/admin/swap" style="color:#bdc3c7;text-decoration:none;display:block;padding:12px 25px;">SWAP</a>\n    <hr style="border-color: #34495e;">'

if target in c:
    c = c.replace(target, swap_link)
    open("E:/wbank/templates/admin/index.html", "w", encoding="utf-8").write(c)
    print("OK - swap hyperlink added")
else:
    print("Pattern not found!")
    print(f"Looking for: {repr(target[:50])}...")
