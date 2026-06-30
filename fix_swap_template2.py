"""Fix quote escaping - use backtick template literals to avoid all quoting issues"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

tpl = open("E:/wbank/templates/admin/swap.html", "r", encoding="utf-8").read()

# Replace the whole row generation section
old = """            if (st === 'Pending') {
                h += '<span style="color:#27ae60;cursor:pointer" onclick="doApprove('+r.id+',&quot;approve&quot;)">[Approve]</span> ';
                h += '<span style="color:#e74c3c;cursor:pointer" onclick="doApprove('+r.id+',&quot;reject&quot;)">[Reject]</span>';
            } else {
                h += '<span style="color:#64748b">Done</span>';
            }"""

new = """            if (st === 'Pending') {
                var a1 = 'doApprove('+r.id+',"approve")';
                var a2 = 'doApprove('+r.id+',"reject")';
                h += '<span style="color:#27ae60;cursor:pointer" onclick="'+a1+'">[Approve]</span> ';
                h += '<span style="color:#e74c3c;cursor:pointer" onclick="'+a2+'">[Reject]</span>';
            } else {
                h += '<span style="color:#64748b">Done</span>';
            }"""

if old in tpl:
    tpl = tpl.replace(old, new)
    open("E:/wbank/templates/admin/swap.html", "w", encoding="utf-8").write(tpl)
    print("OK - fixed")
else:
    print("Pattern not found!")
    import re
    matches = re.findall(r'doApprove[^;]+', tpl)
    for m in matches:
        print(f"  {m[:80]}")
