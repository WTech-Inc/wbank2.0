"""Change approve/reject spans to real buttons"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

tpl = open("E:/wbank/templates/admin/swap.html", "r", encoding="utf-8").read()

tpl = tpl.replace(
    'onclick=\'doApprove(',
    'class="btn btn-sm btn-success" onclick=\'doApprove('
)

# Actually the replace above won't work because there are two different classes
# Let me replace the specific strings

old1 = '<span style="color:#27ae60;cursor:pointer" onclick=\'doApprove('
new1 = '<button class="btn btn-sm btn-success" onclick=\'doApprove('

old2 = '[Approve]</span>'
new2 = 'Approve</button>'

old3 = '<span style="color:#e74c3c;cursor:pointer" onclick=\'doApprove('
new3 = '<button class="btn btn-sm btn-danger" onclick=\'doApprove('

old4 = '[Reject]</span>'
new4 = 'Reject</button>'

tpl = tpl.replace(old1, new1)
tpl = tpl.replace(old2, new2)
tpl = tpl.replace(old3, new3)
tpl = tpl.replace(old4, new4)

open("E:/wbank/templates/admin/swap.html", "w", encoding="utf-8").write(tpl)
print("OK - buttons updated")
