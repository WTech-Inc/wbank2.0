"""Replace entire admin_swap_page function with clean version"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

# Read current file
with open("E:/wbank/main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find the function boundaries
start = content.find("def admin_swap_page():")
end = content.find("def wbank_wtech_find_page", start)

if start < 0 or end < 0:
    print("Could not find function boundaries!")
    sys.exit(1)

# Write the new function to a temp file
new_func = """def admin_swap_page():
    if "admin_user" not in session:
        return redirect("/admin")
    swaps = cashout.query.order_by(cashout.id.desc()).all()
    rows = []
    for s in swaps:
        audit = audit_log.query.filter_by(username=s.name, action='SWAP_APPLY').order_by(audit_log.timestamp.desc()).first()
        rows.append({'id': s.id, 'user': s.name, 'amount': s.amount, 'status': s.status, 'detail': audit.detail if audit else ''})
    rate = swap_config.query.first()
    wtc_r = rate.rate_wtc if rate else 10
    hkd_r = rate.rate_hkd if rate else 1
    fee_p = rate.fee_percent if rate else 10
    rows_html = ''
    for r in rows:
        st = r['status'] or 'Pending'
        det = (r['detail'] or '').replace("'", "&#39;")
        amt = str(r['amount'] or 0)
        rows_html += '<tr>'
        rows_html += '<td>' + str(r['id']) + '</td>'
        rows_html += '<td>' + str(r['user']) + '</td>'
        rows_html += '<td>HK$' + amt + '</td>'
        rows_html += '<td>' + st + '</td>'
        rows_html += '<td style="font-size:11px;color:#64748b;">' + det + '</td>'
        rows_html += '<td>'
        if 'Pending' in st:
            rows_html += '<form style="display:inline" method="POST" action="/admin/api/approve_swap" onsubmit="return confirm(\'Confirm this withdrawal? HK$' + amt + ' cash\')">'
            rows_html += '<input type="hidden" name="id" value="' + str(r['id']) + '">'
            rows_html += '<input type="hidden" name="action" value="approve">'
            rows_html += '<button class="btn btn-success btn-sm" type="submit">Approve</button>'
            rows_html += '</form> '
            rows_html += '<form style="display:inline" method="POST" action="/admin/api/approve_swap">'
            rows_html += '<input type="hidden" name="id" value="' + str(r['id']) + '">'
            rows_html += '<input type="hidden" name="action" value="reject">'
            rows_html += '<button class="btn btn-danger btn-sm" type="submit">Reject</button>'
            rows_html += '</form>'
        else:
            rows_html += '<span style="color:#64748b;">Done</span>'
        rows_html += '</td></tr>'
    if not rows:
        rows_html = '<tr><td colspan="6" style="text-align:center;color:#64748b;padding:40px;">No swap requests</td></tr>'
    h = '<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8">'
    h += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    h += '<title>WBank Swap Admin</title>'
    h += '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">'
    h += '<style>body{background:#f5f6fa;font-family:Segoe UI,sans-serif;padding:20px;}.card{background:white;border-radius:10px;padding:20px;margin-bottom:20px;box-shadow:0 2px 10px rgba(0,0,0,0.05);}table{width:100%;border-collapse:collapse;}th,td{padding:8px 12px;text-align:left;border-bottom:1px solid #e2e8f0;}th{background:#f8fafc;font-size:13px;color:#64748b;}</style></head><body>'
    h += '<div class="container">'
    h += '<h2 style="margin-bottom:20px;">WTC/HKD Swap Admin</h2>'
    h += '<a href="/admin/dashboard" style="font-size:13px;color:#3498db;text-decoration:none;">Back to Admin</a>'
    h += '<div class="card"><h3>Exchange Rate</h3>'
    h += '<div style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;">'
    h += '<div><label style="font-size:12px;color:#64748b;display:block;">WTC</label><input type="number" id="r-wtc" value="' + str(wtc_r) + '" class="form-control form-control-sm" style="width:70px;"></div>'
    h += '<div style="padding-bottom:8px;"><span style="font-size:18px;">=</span></div>'
    h += '<div><label style="font-size:12px;color:#64748b;display:block;">HKD</label><input type="number" id="r-hkd" value="' + str(hkd_r) + '" class="form-control form-control-sm" style="width:70px;"></div>'
    h += '<div><label style="font-size:12px;color:#64748b;display:block;">Fee %</label><input type="number" id="r-fee" value="' + str(fee_p) + '" class="form-control form-control-sm" style="width:70px;"></div>'
    h += '<div style="padding-bottom:8px;"><button class="btn btn-primary btn-sm" onclick="upd()">Update</button><span id="r-msg" style="font-size:12px;color:#27ae60;margin-left:8px;"></span></div>'
    h += '</div></div>'
    h += '<div class="card"><h3>Withdrawal Requests</h3>'
    h += '<table class="table"><thead><tr><th>ID</th><th>User</th><th>HKD</th><th>Status</th><th>Detail</th><th>Action</th></tr></thead><tbody>'
    h += rows_html
    h += '</tbody></table></div></div>'
    h += '<script>function upd(){var w=document.getElementById("r-wtc").value;var h=document.getElementById("r-hkd").value;var f=document.getElementById("r-fee").value;var x=new XMLHttpRequest();x.onreadystatechange=function(){if(x.readyState==4&&x.status==200){document.getElementById("r-msg").textContent="Updated!";setTimeout(function(){document.getElementById("r-msg").textContent="";},3000);}};x.open("POST","/admin/api/swap_rate",true);x.setRequestHeader("Content-Type","application/json");x.send(JSON.stringify({wtc:parseInt(w),hkd:parseInt(h),fee:parseInt(f)}));}</script>'
    h += '</body></html>'
    return h
"""

# Replace the function
new_content = content[:start] + new_func + content[end:]

with open("E:/wbank/main.py", "w", encoding="utf-8") as f:
    f.write(new_content)

# Verify syntax
import py_compile
try:
    py_compile.compile("E:/wbank/main.py", doraise=True)
    print("OK - function replaced, syntax verified")
except Exception as e:
    print(f"SYNTAX ERROR: {e}")
