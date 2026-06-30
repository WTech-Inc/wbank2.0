"""Rebuild swap admin template from scratch - clean, no quoting issues"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

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
        <div style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;">
            <div><label style="font-size:12px;color:#64748b;display:block;">WTC</label><input type="number" id="r-wtc" value="10" class="form-control form-control-sm" style="width:70px;"></div>
            <div style="padding-bottom:8px;"><span style="font-size:18px;">=</span></div>
            <div><label style="font-size:12px;color:#64748b;display:block;">HKD</label><input type="number" id="r-hkd" value="1" class="form-control form-control-sm" style="width:70px;"></div>
            <div><label style="font-size:12px;color:#64748b;display:block;">Fee %</label><input type="number" id="r-fee" value="10" class="form-control form-control-sm" style="width:70px;"></div>
            <div style="padding-bottom:8px;">
                <button class="btn btn-primary btn-sm" onclick="upd()">Update</button>
                <span id="r-msg" style="font-size:12px;color:#27ae60;"></span>
            </div>
        </div>
    </div>

    <div class="card">
        <h3>Withdrawal Requests</h3>
        <div id="data">Loading...</div>
    </div>
</div>

<script>
function load() {
    var x = new XMLHttpRequest();
    x.onreadystatechange = function() {
        if (x.readyState == 4) {
            if (x.status == 200) {
                var rows = JSON.parse(x.responseText);
                var h = '<table class="table"><tr><th>ID</th><th>User</th><th>HKD</th><th>Status</th><th>Detail</th><th>Action</th></tr>';
                for (var i = 0; i < rows.length; i++) {
                    var r = rows[i];
                    var st = r.status || 'Pending';
                    h += '<tr>';
                    h += '<td>' + (r.id||'') + '</td>';
                    h += '<td>' + (r.user||'') + '</td>';
                    h += '<td>HK$' + (r.amount||0) + '</td>';
                    h += '<td>' + st + '</td>';
                    h += '<td style="font-size:11px;color:#64748b;">' + (r.detail||'-') + '</td>';
                    h += '<td>';
                    if (st === 'Pending') {
                        h += '<button class="btn btn-success btn-sm" onclick="app(' + r.id + ',\\\'approve\\\')">Approve</button> ';
                        h += '<button class="btn btn-danger btn-sm" onclick="app(' + r.id + ',\\\'reject\\\')">Reject</button>';
                    } else {
                        h += '<span style="color:#64748b;">Done</span>';
                    }
                    h += '</td></tr>';
                }
                h += '</table>';
                document.getElementById('data').innerHTML = h;
            } else {
                document.getElementById('data').innerHTML = 'Error loading data';
            }
        }
    };
    x.open('GET', '/admin/api/swaps', true);
    x.send();
}

function app(id, action) {
    if (action === 'approve' && !confirm('Approve this withdrawal?')) return;
    var x = new XMLHttpRequest();
    x.onreadystatechange = function() {
        if (x.readyState == 4 && x.status == 200) {
            var d = JSON.parse(x.responseText);
            if (d.success) load();
        }
    };
    x.open('POST', '/admin/api/approve_swap', true);
    x.setRequestHeader('Content-Type', 'application/json');
    x.send(JSON.stringify({id:id, action:action}));
}

function upd() {
    var w = document.getElementById('r-wtc').value;
    var h = document.getElementById('r-hkd').value;
    var f = document.getElementById('r-fee').value;
    var x = new XMLHttpRequest();
    x.onreadystatechange = function() {
        if (x.readyState == 4 && x.status == 200) {
            document.getElementById('r-msg').textContent = 'Updated!';
            setTimeout(function(){document.getElementById('r-msg').textContent='';},3000);
        }
    };
    x.open('POST', '/admin/api/swap_rate', true);
    x.setRequestHeader('Content-Type', 'application/json');
    x.send(JSON.stringify({wtc:parseInt(w), hkd:parseInt(h), fee:parseInt(f)}));
}

load();
</script>
</body>
</html>"""

with open("E:/wbank/templates/admin/swap.html", "w", encoding="utf-8") as f:
    f.write(tpl)
print("OK - template rebuilt")
