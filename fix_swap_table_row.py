"""Fix swap table rows in admin template - add detail column"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

old = """swaps.map(s =>
                    '<tr><td>' + s.id + '</td><td>' + s.user + '</td><td>HK$' + s.amount + '</td><td>' + (s.status || 'Pending') + '</td>' +
                    '<td>' + ((s.status || 'Pending') === 'Pending' ?"""

new = """swaps.map(s =>
                    '<tr><td>' + s.id + '</td><td>' + (s.user || '') + '</td><td>HK$' + (s.amount || 0) + '</td><td>' + (s.status || 'Pending') + '</td>' +
                    '<td style="font-size:11px;color:#64748b;max-width:200px;overflow:hidden;text-overflow:ellipsis;">' + (s.detail || '-') + '</td>' +
                    '<td>' + ((s.status || 'Pending') === 'Pending' ?"""

if old in c:
    c = c.replace(old, new)
    open(path, "w", encoding="utf-8").write(c)
    print("OK - swap table rows fixed")
else:
    print("NOT FOUND")
    # Show what's actually there
    idx = c.find("swaps.map")
    if idx >= 0:
        print(repr(c[idx:idx+400]))
