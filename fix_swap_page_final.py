"""Replace embedded swap page with template render + create template file"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

# Create template file
tpl = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WBank Swap Admin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background:#f5f6fa; font-family:Segoe UI,sans-serif; padding:20px; }
        .card { background:white; border-radius:10px; padding:20px; margin-bottom:20px; box-shadow:0 2px 10px rgba(0,0,0,0.05); }
        .rate-group { display:flex; gap:12px; align-items:end; flex-wrap:wrap; }
        .rate-group label { font-size:12px; color:#64748b; display:block; }
        .rate-group input { width:70px; }
        table { width:100%; border-collapse:collapse; }
        th, td { padding:8px 12px; text-align:left; border-bottom:1px solid #e2e8f0; }
        th { background:#f8fafc; font-size:13px; color:#64748b; }
    </style>
</head>
<body>
<div class="container">
    <h2 style="margin-bottom:20px;">WTC/HKD Swap Admin</h2>
    <a href="/admin/dashboard" style="font-size:13px;color:#3498db;text-decoration:none;">Back to Admin</a>

    <div class="card">
        <h3>Exchange Rate</h3>
        <div class="rate-group">
            <div><label>WTC</label><input type="number" id="rate-wtc" value="10" class="form-control form-control-sm"></div>
            <div style="padding-bottom:8px;"><span style="font-size:18px;">=</span></div>
            <div><label>HKD</label><input type="number" id="rate-hkd" value="1" class="form-control form-control-sm"></div>
            <div><label>Fee %</label><input type="number" id="rate-fee" value="10" class="form-control form-control-sm"></div>
            <div style="padding-bottom:8px;">
                <button class="btn btn-primary btn-sm" onclick="updateRate()">Update</button>
                <span id="rate-status" style="font-size:12px;color:#27ae60;"></span>
            </div>
        </div>
    </div>

    <div class="card">
        <h3>Withdrawal Requests</h3>
        <div id="swap-data">Loading...</div>
    </div>
</div>

<script>
function loadData() {
    fetch('/admin/api/swaps').then(function(r){return r.json()}).then(function(rows){
        var h = '<table class="table"><tr><th>ID</th><th>User</th><th>HKD</th><th>Status</th><th>Detail</th><th>Action</th></tr>';
        for (var i = 0; i < rows.length; i++) {
            var r = rows[i];
            var st = r.status || 'Pending';
            var detail = (r.detail || '-').replace(/'/g,"&#39;");
            h += '<tr>';
            h += '<td>'+(r.id||'')+'</td><td>'+(r.user||'')+'</td><td>HK$'+(r.amount||0)+'</td><td>'+st+'</td>';
            h += '<td style="font-size:11px;color:#64748b;">'+detail+'</td><td>';
            if (st === 'Pending') {
                h += '<span style="color:#27ae60;cursor:pointer" onclick="doApprove('+r.id+',&quot;approve&quot;)">[Approve]</span> ';
                h += '<span style="color:#e74c3c;cursor:pointer" onclick="doApprove('+r.id+',&quot;reject&quot;)">[Reject]</span>';
            } else {
                h += '<span style="color:#64748b">Done</span>';
            }
            h += '</td></tr>';
        }
        h += '</table>';
        document.getElementById('swap-data').innerHTML = h;
    }).catch(function(e){
        document.getElementById('swap-data').innerHTML = 'Error: '+e.message;
    });
}
function doApprove(id, action) {
    if (action === 'approve' && !confirm('Approve this withdrawal?')) return;
    fetch('/admin/api/approve_swap',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:id,action:action})})
    .then(function(r){return r.json()}).then(function(d){if(d.success)loadData();}).catch(function(e){alert(e.message);});
}
function updateRate() {
    var f = document.getElementById;
    fetch('/admin/api/swap_rate',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({wtc:parseInt(f('rate-wtc').value),hkd:parseInt(f('rate-hkd').value),fee:parseInt(f('rate-fee').value)})})
    .then(function(r){return r.json()}).then(function(d){
        f('rate-status').textContent = d.success ? 'Updated!' : 'Error';
        setTimeout(function(){f('rate-status').textContent='';},3000);
    }).catch(function(e){f('rate-status').textContent='Error';});
}
loadData();
</script>
</body>
</html>"""

with open("E:/wbank/templates/admin/swap.html", "w", encoding="utf-8") as f:
    f.write(tpl)
print("Template created")

# Update main.py to use render_template instead of hardcoded string
main = open("E:/wbank/main.py", "r", encoding="utf-8").read()

old_func = '''@app.route("/admin/swap")
@csrf.exempt
def admin_swap_page():
    """Standalone swap management page"""
    if "admin_user" not in session:
        return redirect("/admin")
    return \\'\\'\\'<!DOCTYPE html>'''

new_func = '''@app.route("/admin/swap")
@csrf.exempt
def admin_swap_page():
    """Standalone swap management page"""
    if "admin_user" not in session:
        return redirect("/admin")
    return render_template("admin/swap.html")'''

if old_func in main:
    main = main.replace(old_func, new_func)
    # Also remove everything between the template start and end
    start = main.find("return render_template")
    end = main.find("'''", start + 100)
    if end > 0:
        # Find the end of the triple-quoted string (the closing ''')
        # It should be near the end of the function
        end2 = main.find("'''", end + 3)
        if end2 > 0:
            # Remove the old HTML string and the extra '''
            main = main[:start] + "return render_template(\"admin/swap.html\")" + main[end2+3:]
            open("E:/wbank/main.py", "w", encoding="utf-8").write(main)
            print("main.py updated")
        else:
            print("Could not find closing triple quotes")
    else:
        print("Could not find insertion point after render_template")
else:
    print("Function pattern not found - checking for other patterns")
    if "admin_swap_page" in main:
        print("admin_swap_page exists")
        idx = main.find("admin_swap_page")
        print(f"Found at {idx}: {main[idx:idx+100]}")
