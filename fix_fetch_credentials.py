"""Add credentials: 'include' to swap apply fetch"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/wbankClient.html"
c = open(path, "r", encoding="utf-8").read()

old = "body: JSON.stringify({amount: amt})"
new = "body: JSON.stringify({amount: amt}), credentials: 'include'"

if old in c:
    c = c.replace(old, new)
    open(path, "w", encoding="utf-8").write(c)
    print("Fixed - added credentials: include")
else:
    print("Pattern not found")
    # Show what's around that area
    idx = c.find("swap/apply")
    if idx >= 0:
        print(c[idx-50:idx+100])
