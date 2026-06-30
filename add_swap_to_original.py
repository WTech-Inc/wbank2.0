"""Carefully add swap section + JS to original admin template"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# 1. Add swap section HTML BEFORE <script>
swap_html = """    <!-- Swap Section -->
    <div id="section-swap" class="section">
        <div class="stat-card">
            <h4>💱 WTC/HKD Swap - Exchange Rate</h4>
            <div class="row mb-3">
                <div class="col-md-2">
                    <label style="font-size:12px;color:#64748b;">WTC</label>
                    <input type="number" class="form-control form-control-sm" id="rate-wtc" value="10">
                </div>
                <div class="col-md-1" style="display:flex;align-items:end;justify-content:center;padding-bottom:8px;">
                    <span style="font-size:18px;">=</span>
                </div>
                <div class="col-md-2">
                    <label style="font-size:12px;color:#64748b;">HKD</label>
                    <input type="number" class="form-control form-control-sm" id="rate-hkd" value="1">
                </div>
                <div class="col-md-2">
                    <label style="font-size:12px;color:#64748b;">Fee %</label>
                    <input type="number" class="form-control form-control-sm" id="rate-fee" value="10">
                </div>
                <div class="col-md-3" style="display:flex;align-items:end;padding-bottom:8px;">
                    <button class="btn btn-primary btn-sm" onclick="updateSwapRate()">Update</button>
                    <span id="rate-status" style="font-size:12px;color:#27ae60;margin-left:8px;"></span>
                </div>
            </div>
        </div>
        <div class="stat-card">
            <h4>Calculator</h4>
            <div class="row mb-3">
                <div class="col-md-3">
                    <input type="number" class="form-control form-control-sm" id="calc-wtc" placeholder="WTC amount">
                </div>
                <div class="col-md-2">
                    <button class="btn btn-success btn-sm" onclick="calcSwap()">Calculate</button>
                </div>
            </div>
            <div id="calc-result" style="font-size:14px;color:#2c3e50;"></div>
        </div>
        <div class="table-container">
            <h4>Withdrawal Requests (WTC to HKD)</h4>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead><tr><th>ID</th><th>User</th><th>HKD</th><th>Status</th><th>Detail</th><th>Action</th></tr></thead>
                    <tbody id="swap-table-body"><tr><td colspan="6" class="loading">Loading...</td></tr></tbody>
                </table>
            </div>
        </div>
    </div>

"""

# Insert before <script>
c = c.replace("<script>", swap_html + "<script>")
print("Swap HTML added")

# 2. Add swap JS before </script>
swap_js = """
        // === Swap Functions ===
        async function loadSwapData() {
            try { var r = await fetch('/admin/api/swap_rate'); var d = await r.json();
                if (document.getElementById('rate-wtc')) document.getElementById('rate-wtc').value = d.wtc;
                if (document.getElementById('rate-hkd')) document.getElementById('rate-hkd').value = d.hkd;
                if (document.getElementById('rate-fee')) document.getElementById('rate-fee').value = d.fee;
            } catch(e) {}
            try { var r = await fetch('/admin/api/swaps'); var swaps = await r.json();
                var tb = document.getElementById('swap-table-body'); if (!tb) return;
                if (!swaps || swaps.length === 0) { tb.innerHTML = '<tr><td colspan="6">No requests</td></tr>'; return; }
                var html = '';
                for (var i = 0; i < swaps.length; i++) {
                    var s = swaps[i];
                    html += '<tr><td>'+(s.id||'')+'</td><td>'+(s.user||'')+'</td><td>HK$'+(s.amount||0)+'</td><td>'+(s.status||'Pending')+'</td>';
                    html += '<td style="font-size:11px;color:#64748b;max-width:200px;overflow:hidden;">'+(s.detail||'-')+'</td>';
                    html += '<td>';
                    if ((s.status||'Pending') === 'Pending') {
                        html += '<button class="btn btn-success btn-sm" onclick="approveSwap('+s.id+",'approve')\">Approve</button> ";
                        html += '<button class="btn btn-danger btn-sm" onclick="approveSwap('+s.id+",'reject')\">Reject</button>";
                    } else {
                        html += '<span style="color:#64748b;">Done</span>';
                    }
                    html += '</td></tr>';
                }
                tb.innerHTML = html;
            } catch(e) { console.log('Swap error:', e); }
        }
        async function updateSwapRate() {
            var btn = event.target; btn.disabled = true; btn.innerHTML = 'Saving...';
            try { var r = await fetch('/admin/api/swap_rate', { method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({ wtc: parseInt(document.getElementById('rate-wtc').value),
                    hkd: parseInt(document.getElementById('rate-hkd').value),
                    fee: parseInt(document.getElementById('rate-fee').value) }) });
                var d = await r.json();
                document.getElementById('rate-status').textContent = d.success ? 'Updated!' : 'Error';
            } catch(e) { document.getElementById('rate-status').textContent = 'Error'; }
            btn.disabled = false; btn.innerHTML = 'Update';
            setTimeout(function(){ document.getElementById('rate-status').textContent = ''; }, 3000);
        }
        async function approveSwap(id, action) {
            try { var r = await fetch('/admin/api/approve_swap', { method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({id: id, action: action}) });
                var d = await r.json();
                if (d.success) loadSwapData();
            } catch(e) { alert('Error: ' + e.message); }
        }
        function calcSwap() {
            var wtc = parseFloat(document.getElementById('calc-wtc').value);
            if (!wtc || wtc <= 0) { document.getElementById('calc-result').innerHTML = ''; return; }
            var rw = parseInt(document.getElementById('rate-wtc').value);
            var rh = parseInt(document.getElementById('rate-hkd').value);
            var f = parseInt(document.getElementById('rate-fee').value);
            var g = wtc * rh / rw; var fa = g * f / 100; var n = g - fa;
            document.getElementById('calc-result').innerHTML =
                '<div style="background:#f0fdf4;padding:12px;border-radius:8px;"><b>'+wtc+' WTC</b> &rarr; <b>HK$'+n.toFixed(2)+'</b><br>'+
                '<span style="font-size:12px;color:#64748b;">Gross: HK$'+g.toFixed(2)+' | Fee ('+f+'%): HK$'+fa.toFixed(2)+'</span></div>';
        }
        // Add swap support to showSection
        var origShow = showSection;
        showSection = function(id, el) {
            origShow(id, el);
            if (id === 'swap') setTimeout(loadSwapData, 100);
        };
"""

c = c.replace("</script>", swap_js + "\n</script>")
print("Swap JS added")

open(path, "w", encoding="utf-8").write(c)
print(f"Done - {len(c)} bytes")
