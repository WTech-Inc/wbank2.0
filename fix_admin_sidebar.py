"""Add swap link to admin sidebar"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

swap_link = '<a href="#" onclick="showSection(\'swap\', this)"><i class="bi bi-currency-exchange"></i> WTC/HKD Swap</a>'

if swap_link in c:
    print("Swap link already exists")
    sys.exit(0)

old = '<div class="nav-section">Data</div>'
new = swap_link + '\n    ' + old

if old in c:
    c = c.replace(old, new)
    open(path, "w", encoding="utf-8").write(c)
    print("OK - swap link added")
else:
    print("Pattern not found")
