"""Fix onclick in swap template - use single quotes for onclick attr"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

tpl = open("E:/wbank/templates/admin/swap.html", "r", encoding="utf-8").read()

# Remove intermediate variables and fix onclick
old_block = """            if (st === 'Pending') {
                var a1 = 'doApprove('+r.id+',"approve")';
                var a2 = 'doApprove('+r.id+',"reject")';
                h += '<span style="color:#27ae60;cursor:pointer" onclick="'+a1+'">[Approve]</span> ';
                h += '<span style="color:#e74c3c;cursor:pointer" onclick="'+a2+'">[Reject]</span>';
            } else {
                h += '<span style="color:#64748b">Done</span>';
            }"""

new_block = """            if (st === 'Pending') {
                h += '<span style="color:#27ae60;cursor:pointer" onclick=\\'doApprove('+r.id+',\\\\'approve\\\\')\\'\\'>[Approve]</span> ';
                h += '<span style="color:#e74c3c;cursor:pointer" onclick=\\'doApprove('+r.id+',\\\\'reject\\\\')\\'\\'>[Reject]</span>';
            } else {
                h += '<span style="color:#64748b">Done</span>';
            }"""

# Actually let me just use a completely different approach: use double-quote JS strings
# So the onclick attribute uses single quotes
new_block2 = """            if (st === 'Pending') {
                h += "<span style=\\"color:#27ae60;cursor:pointer\\" onclick='doApprove("+r.id+",\\"approve\\")'>[Approve]</span> ";
                h += "<span style=\\"color:#e74c3c;cursor:pointer\\" onclick='doApprove("+r.id+",\\"reject\\")'>[Reject]</span>";
            } else {
                h += '<span style="color:#64748b">Done</span>';
            }"""

if old_block in tpl:
    tpl = tpl.replace(old_block, new_block2)
    open("E:/wbank/templates/admin/swap.html", "w", encoding="utf-8").write(tpl)
    print("OK")
else:
    print("NOT FOUND!")
    print(repr(tpl[tpl.find("Pending"):tpl.find("Pending")+300]))
