"""Add only the swap sidebar link to admin template - minimal change"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8").read()

old = """    <a href="#" onclick="showSection('audit', this)">📋 Audit Log</a>"""
new = """    <a href="#" onclick="showSection('audit', this)">📋 Audit Log</a>
        <a href="#" onclick="showSection('swap', this)">💱 WTC/HKD Swap</a>"""

if old in c:
    c = c.replace(old, new)
    open("E:/wbank/templates/admin/index.html", "w", encoding="utf-8").write(c)
    print("OK - swap link added")
else:
    print("Pattern not found!")
    # Debug
    idx = c.find("Audit Log")
    if idx >= 0:
        print(repr(c[idx-40:idx+40]))
