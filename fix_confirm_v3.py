"""Add confirm dialog using intermediate var"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/main.py", "r", encoding="utf-8").read()

# Find and replace the whole approve button line
idx = c.find("Approve</button>")
line_start = c.rfind("\n", 0, idx) + 1
line_end = c.find("\n", idx)

old_line = c[line_start:line_end]
print(f"Old line: {old_line[:80]}...")

# Build new line: add a variable for the amount check, then use it in onclick
new_line = old_line.replace('type="submit">Approve</button>', 'type="submit" onclick="return confirm(\\'HK$\\'+window.amount_'+'${r[\"id\"]}'+'||\\'?\\'+\\' cash?\\')">Approve</button>')

# Actually that's still complex. Let me use a different approach.
# Just add a simple global JS confirm

# Replace whole function with hardcoded fix
old_func_start = c.find("rows_html += '<td>' + str(r['id']) + '</td>'")
# Find the approve button line within the function
btn_old = """rows_html += '<button class="btn btn-success btn-sm" type="submit">Approve</button>'"""
btn_new = """rows_html += '<button class="btn btn-success btn-sm" type="submit" onclick=\\'return confirm(\\\"Confirm this withdrawal? HK\\$' + str(r['amount'] or 0) + '\\\")\\'>Approve</button>'"""

if btn_old in c:
    c = c.replace(btn_old, btn_new)
    open("E:/wbank/main.py", "w", encoding="utf-8").write(c)
    print("OK - confirm added")
else:
    print("Pattern not found!")
    # Show what's actually there
    idx2 = c.find("btn-success")
    if idx2 >= 0:
        print(f"Found at {idx2}: {c[idx2-20:idx2+80]}")
