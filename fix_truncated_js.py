"""Fix truncated JS line in wbankClient.html"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/wbankClient.html"
c = open(path, "r", encoding="utf-8").read()

# The broken line is incomplete - find and fix it
old = 'result.innerHTML = \'<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">\' \n                }'
new = 'result.innerHTML = \'<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">\' + (d.error || \'Swap failed\') + \'</div>\';\n                }'

if old in c:
    c = c.replace(old, new)
    print("Fixed truncated JS line")
else:
    print("Pattern not found, trying alternative...")
    # Try just the line itself
    for i, line in enumerate(c.split("\n")):
        if "result.innerHTML" in line and "background:#fef2f2" in line and "Swap" not in line:
            print(f"Found incomplete line {i+1}: {line.strip()[:80]}")
            # Replace just this line
            old_line = line
            new_line = line.strip() + " + (d.error || 'Swap failed') + '</div>';"
            c = c.replace(old_line, new_line)
            print("Fixed!")
            break

open(path, "w", encoding="utf-8").write(c)
print(f"Saved ({len(c)} bytes)")
