"""Fix swap approve/reject button JS to avoid quoting issues"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# Find and replace the button generation code
old = '''                    if ((s.status||'Pending') === 'Pending') {
                        html += '<button class="btn btn-success btn-sm" onclick="approveSwap('+s.id+",'approve')\">Approve</button> ";
                        html += '<button class="btn btn-danger btn-sm" onclick="approveSwap('+s.id+",'reject')\">Reject</button>";
                    } else {
                        html += '<span style="color:#64748b;">Done</span>';
                    }'''

new = '''                    if ((s.status||'Pending') === 'Pending') {
                        html += '<span class="text-success" style="cursor:pointer;" onclick="approveSwap('+s.id+',\\'approve\\')">[Approve]</span> ';
                        html += '<span class="text-danger" style="cursor:pointer;" onclick="approveSwap('+s.id+',\\'reject\\')">[Reject]</span>';
                    } else {
                        html += '<span style="color:#64748b;">Done</span>';
                    }'''

if old in c:
    c = c.replace(old, new)
    open(path, "w", encoding="utf-8").write(c)
    print("Fixed button generation")
else:
    print("Pattern not found!")
    # Debug
    idx = c.find("btn-success btn-sm")
    if idx >= 0:
        print(f"Found at {idx}: {c[idx:idx+200]}")
    else:
        idx = c.find("approveSwap")
        if idx >= 0:
            print(f"Found approveSwap at {idx}: {c[idx-20:idx+100]}")
