"""Fix swap approve/reject button JS syntax"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# Replace the broken button HTML with simpler version
old = """? '<button onclick="approveSwap(' + s.id + ",'approve')" style="background:#27ae60;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;">Approve</button> "
                        + '<button onclick="approveSwap(' + s.id + ",'reject')" style="background:#e74c3c;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;">Reject</button>'"""

new = """? '<button class="btn btn-success btn-sm" onclick="approveSwap(' + s.id + ",'approve')" + '">Approve</button> '
                        + '<button class="btn btn-danger btn-sm" onclick="approveSwap(' + s.id + ",'reject')" + '">Reject</button>'"""

if old in c:
    c = c.replace(old, new)
    print("Fixed approve/reject buttons")
else:
    print("Pattern not found!")
    # Show what's near that area
    idx = c.find("Approve</button>")
    if idx >= 0:
        print(f"Found at {idx}:")
        print(c[idx-100:idx+200])

open(path, "w", encoding="utf-8").write(c)
print("Saved")
