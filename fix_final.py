"""Fix swap JS - simplify approveSwap calls"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

# Read the file as raw bytes to avoid encoding issues
with open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8") as f:
    c = f.read()

# Remove the broken approveSwap calls with replace
old1 = "html += '<span class=\"text-success\" style=\"cursor:pointer;\" onclick=\"approveSwap('+s.id+",'approve',"+s.amount+",'"+s.detail.replace(/'/g,"")+"')\">[Approve]</span> ';"
new1 = "html += '<span class=\"text-success\" style=\"cursor:pointer;\" onclick=\"approveSwap('+s.id+",'approve')\">[Approve]</span> ';"

old2 = "html += '<span class=\"text-danger\" style=\"cursor:pointer;\" onclick=\"approveSwap('+s.id+",'reject',"+s.amount+",'"+s.detail.replace(/'/g,"")+"')\">[Reject]</span>';"
new2 = "html += '<span class=\"text-danger\" style=\"cursor:pointer;\" onclick=\"approveSwap('+s.id+",'reject')\">[Reject]</span>';"

c = c.replace(old1, new1)
c = c.replace(old2, new2)

# Simplify approveSwap function to just show amount from detail
old_func = """        async function approveSwap(id, action, amount, detail) {
            if (action === 'approve') {
                var msg = 'User will receive: HK$' + (amount || '?') + ' in cash\\n\\n' + (detail || '');
                if (!confirm(msg + '\\n\\nConfirm this withdrawal?')) return;
            }
            try { var r = await fetch('/admin/api/approve_swap', { method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({id: id, action: action}) });
                var d = await r.json();
                if (d.success) loadSwapData();
            } catch(e) { alert('Error: ' + e.message); }
        }"""

new_func = """        async function approveSwap(id, action) {
            try { var r = await fetch('/admin/api/approve_swap', { method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({id: id, action: action}) });
                var d = await r.json();
                if (d.success) loadSwapData();
            } catch(e) { alert('Error: ' + e.message); }
        }"""

c = c.replace(old_func, new_func)

with open("E:/wbank/templates/admin/index.html", "w", encoding="utf-8") as f:
    f.write(c)
print("Done")
