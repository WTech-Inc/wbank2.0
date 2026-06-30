"""Center swap content and add approve confirmation"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# 1. Center rate control
c = c.replace('display:flex;gap:12px;align-items:end;flex-wrap:wrap;justify-content:center;',
              'display:flex;gap:12px;align-items:end;flex-wrap:wrap;justify-content:center;')

# 2. Center calculator
c = c.replace('display:flex;gap:12px;align-items:center;justify-content:center;',
              'display:flex;gap:12px;align-items:center;justify-content:center;')

# 3. Center table container
c = c.replace('class="table-container">\n            <h4>Withdrawal Requests (WTC to HKD)</h4>',
              'class="table-container" style="text-align:center;">\n            <h4>Withdrawal Requests (WTC to HKD)</h4>')

# 4. Add approve confirmation dialog
old_approve = '''        async function approveSwap(id, action) {
            try { var r = await fetch('/admin/api/approve_swap', { method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({id: id, action: action}) });
                var d = await r.json();
                if (d.success) loadSwapData();
            } catch(e) { alert('Error: ' + e.message); }
        }'''

new_approve = '''        async function approveSwap(id, action, amount, detail) {
            if (action === 'approve') {
                var msg = 'User will receive: HK$' + (amount || '?') + ' in cash\\n\\n' + (detail || '');
                if (!confirm(msg + '\\n\\nConfirm this withdrawal?')) return;
            }
            try { var r = await fetch('/admin/api/approve_swap', { method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({id: id, action: action}) });
                var d = await r.json();
                if (d.success) loadSwapData();
            } catch(e) { alert('Error: ' + e.message); }
        }'''

c = c.replace(old_approve, new_approve)

# 5. Update the table row to pass amount and detail to approveSwap
old_row = '''html += '<td>';
                    if ((s.status||'Pending') === 'Pending') {
                        html += '<span class="text-success" style="cursor:pointer;" onclick="approveSwap('+s.id+',\\'approve\\')">[Approve]</span> ';
                        html += '<span class="text-danger" style="cursor:pointer;" onclick="approveSwap('+s.id+',\\'reject\\')">[Reject]</span>';
                    } else {
                        html += '<span style="color:#64748b;">Done</span>';
                    }'''

new_row = '''html += '<td>';
                    if ((s.status||'Pending') === 'Pending') {
                        html += '<span class="text-success" style="cursor:pointer;" onclick="approveSwap('+s.id+",'approve',"+s.amount+",'"+s.detail.replace(/'/g,"")+"')\">[Approve]</span> ';
                        html += '<span class="text-danger" style="cursor:pointer;" onclick="approveSwap('+s.id+",'reject',"+s.amount+",'"+s.detail.replace(/'/g,"")+"')\">[Reject]</span>';
                    } else {
                        html += '<span style="color:#64748b;">Done</span>';
                    }'''

c = c.replace(old_row, new_row)

open(path, "w", encoding="utf-8").write(c)
print(f"Done - {len(c)} bytes")
