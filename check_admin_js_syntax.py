"""Check admin JS syntax by extracting script block"""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")

lines = open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8").readlines()

# Find script block
in_block = False
js_lines = []
for i, line in enumerate(lines):
    if "<script" in line:
        in_block = True
        continue
    if "</script>" in line:
        break
    if in_block:
        js_lines.append(line)

js = "".join(js_lines)
print(f"JS block: {len(js_lines)} lines, {len(js)} chars")

# Write to temp file and check with Node
tmp = "E:/wbank/_check_admin.js"
with open(tmp, "w", encoding="utf-8") as f:
    f.write(js)

r = os.system(f"node --check {tmp} 2>&1")
if r == 0:
    print("JS SYNTAX: OK")
else:
    print("JS SYNTAX: FAILED")
    # Show the error
    os.system(f"node --check {tmp}")
os.remove(tmp)
