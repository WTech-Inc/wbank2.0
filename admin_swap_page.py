"""Add standalone swap admin page - no modifications to existing admin template"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

# Add a new route to main.py for standalone swap page
main = open("E:/wbank/main.py", "r", encoding="utf-8").read()

if "admin_swap_page" not in main:
    swap_route = '''

@app.route("/admin/swap")
@csrf.exempt
def admin_swap_page():
    """Standalone swap management page"""
    if "admin_user" not in session:
        return redirect("/admin")
    return \'\'\'<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WBank Swap Admin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background:#f5f6fa; font-family:Segoe UI,sans-serif; padding:20px; }
        .card { background:white; border-radius:10px; padding:20px; margin-bottom:20px; box-shadow:0 2px 10px rgba(0,0,0,0.05); }
        .card h3 { margin:0 0 12px 0; color:#2c3e50; }
        .rate-group { display:flex; gap:12px; align-items:end; flex-wrap:wrap; }
        .rate-group label { font-size:12px; color:#64748b; display:block; }
        .rate-group input { width:70px; }
        table { width:100%; border-collapse:collapse; }
        th, td { padding:8px 12px; text-align:left; border-bottom:1px solid #e2e8f0; }
        th { background:#f8fafc; font-size:13px; color:#64748b; }
        .btn-sm { padding:4px 12px; font-size:12px; border:none; border-radius:4px; cursor:pointer; }
        .btn-success { background:#27ae60; color:white; }
        .btn-danger { background:#e74c3c; color:white; }
        .btn-primary { background:#3498db; color:white; }
        .status { font-size:12px; color:#64748b; }
        .flash { padding:12px; border-radius:8px; margin-bottom:12px; text-align:center; }
        .flash-success { background:#d4edda; color:#155724; }
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
                <span id="rate-status" class="status"></span>
            </div>
        </div>
    </div>

    <div class="card" id="calculator" style="display:none;">
        <h3>Calculator</h3>
        <div id="calc-result"></div>
    </div>

    <div class="card">
        <h3>Withdrawal Requests</h3>
        <div id="swap-data">Loading...</div>
    </div>
</div>

<script>
function loadData() {
    var x = new XMLHttpRequest();
    x.onload = function() {
        var swaps = JSON.parse(x.responseText);
        var h = '<table><tr><th>ID</th><th>User</th><th>HKD</th><th>Status</th><th>Detail</th><th>Action</th></tr>';
        for (var i = 0; i < swaps.length; i++) {
            var s = swaps[i];
            var st = s.status || 'Pending';
            h += '<tr>';
            h += '<td>' + (s.id||'') + '</td>';
            h += '<td>' + (s.user||'') + '</td>';
            h += '<td>HK$' + (s.amount||0) + '</td>';
            h += '<td>' + st + '</td>';
            h += '<td style="font-size:11px;color:#64748b;">' + (s.detail||'-') + '</td>';
            h += '<td>';
            if (st === 'Pending') {
                h += '<button class="btn-sm btn-success" onclick="doApprove(' + s.id + ',\\\'approve\\\')">Approve</button> ';
                h += '<button class="btn-sm btn-danger" onclick="doApprove(' + s.id + ',\\\'reject\\\')">Reject</button>';
            } else {
                h += '<span class="status">Done</span>';
            }
            h += '</td></tr>';
        }
        h += '</table>';
        document.getElementById('swap-data').innerHTML = h;
    };
    x.open('GET', '/admin/api/swaps', true);
    x.send();

    var y = new XMLHttpRequest();
    y.onload = function() {
        var d = JSON.parse(y.responseText);
        document.getElementById('rate-wtc').value = d.wtc;
        document.getElementById('rate-hkd').value = d.hkd;
        document.getElementById('rate-fee').value = d.fee;
    };
    y.open('GET', '/admin/api/swap_rate', true);
    y.send();
}

function updateRate() {
    var wtc = document.getElementById('rate-wtc').value;
    var hkd = document.getElementById('rate-hkd').value;
    var fee = document.getElementById('rate-fee').value;
    var z = new XMLHttpRequest();
    z.onload = function() {
        document.getElementById('rate-status').textContent = 'Updated!';
        setTimeout(function(){document.getElementById('rate-status').textContent='';},3000);
    };
    z.open('POST', '/admin/api/swap_rate', true);
    z.setRequestHeader('Content-Type', 'application/json');
    z.send(JSON.stringify({wtc:parseInt(wtc),hkd:parseInt(hkd),fee:parseInt(fee)}));
}

function doApprove(id, action) {
    if (action === 'approve') {
        if (!confirm('Confirm this withdrawal?')) return;
    }
    var z = new XMLHttpRequest();
    z.onload = function() { loadData(); };
    z.open('POST', '/admin/api/approve_swap', true);
    z.setRequestHeader('Content-Type', 'application/json');
    z.send(JSON.stringify({id:id, action:action}));
}

loadData();
</script>
</body>
</html>\'\'\'
'''

    # Insert before the last route
    insert_point = main.rfind("@app.route")
    if insert_point > 0:
        main = main[:insert_point] + swap_route + main[insert_point:]
        open("E:/wbank/main.py", "w", encoding="utf-8").write(main)
        print("OK - standalone swap page added at /admin/swap")
    else:
        print("Could not find insertion point")
else:
    print("Swap page already exists")
