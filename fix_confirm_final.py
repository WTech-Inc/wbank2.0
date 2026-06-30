"""Add confirm dialog to approve button"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/main.py", "r", encoding="utf-8").read()

old = '<button class="btn btn-success btn-sm" type="submit">Approve</button>'
new = '<button class="btn btn-success btn-sm" type="submit" onclick=\\"return confirm(\\'Confirm this withdrawal? HK$' + " + str(r['amount'] or 0) + " + ')\\">Approve</button>"

# Actually, the onclick needs to be generated dynamically with the row amount
# So I need to modify the Python code generation, not the static HTML
# The Python line is: rows_html += '<button ...>Approve</button>'
# I need: rows_html += '<button ... onclick="return confirm(\\'Confirm? HK$'+str(r['amount']or 0)+'\\')">Approve</button>'

old_line = "rows_html += '<button class=\"btn btn-success btn-sm\" type=\"submit\">Approve</button>'"
new_line = "rows_html += '<button class=\"btn btn-success btn-sm\" type=\"submit\" onclick=\\\"return confirm(\\'Confirm this withdrawal? HK$' + str(r['amount'] or 0) + '\\')\\\">Approve</button>'"

if old_line in c:
    c = c.replace(old_line, new_line)
    open("E:/wbank/main.py", "w", encoding="utf-8").write(c)
    print("OK")
else:
    print("Pattern not found!")
    idx = c.find("Approve</button>")
    if idx >= 0:
        print(f"Found at {idx}: {c[idx-80:idx+20]}")
