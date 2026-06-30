"""Cleanly add swap section to admin template - no duplicates"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# 1. Add sidebar link (after Audit Log)
old_sidebar = '<a href="#" onclick="showSection(\'audit\', this)">📋 Audit Log</a>'
new_sidebar = '<a href="#" onclick="showSection(\'audit\', this)">📋 Audit Log</a>\n        <a href="#" onclick="showSection(\'swap\', this)">💱 WTC/HKD Swap</a>'
c = c.replace(old_sidebar, new_sidebar)
print("Sidebar link added")

# 2. Add swap section HTML (before the closing </div> of content, before <script>)
old_end = '<div class="table-container">\n                    <h4 style="margin-bottom:12px;">Export Audit Log</h4>'
swap_html = '''            <div id="section-swap" class="section">
                <div class="admin-header"><h2>💱 WTC/HKD Swap Management</h2></div>

                <div class="stat-card">
                    <h4>Exchange Rate</h4>
                    <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:12px;">
                        <div><label style="font-size:12px;color:#64748b;">WTC</label><input type="number" id="rate-wtc" value="10" style="width:80px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;"></div>
                        <span style="font-size:18px;">=</span>
                        <div><label style="font-size:12px;color:#64748b;">HKD</label><input type="number" id="rate-hkd" value="1" style="width:80px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;"></div>
                        <div><label style="font-size:12px;color:#64748b;">Fee %</label><input type="number" id="rate-fee" value="10" style="width:80px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;"></div>
                        <button onclick="updateSwapRate()" style="background:#3498db;color:white;border:none;padding:8px 20px;border-radius:6px;cursor:pointer;">Update Rate</button>
                        <span id="rate-status" style="font-size:12px;color:#27ae60;"></span>
                    </div>
                </div>

                <div class="stat-card">
                    <h4>Calculator</h4>
                    <div style="display:flex;gap:16px;align-items:center;margin-top:12px;">
                        <input type="number" id="calc-wtc" placeholder="WTC amount" style="width:200px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;">
                        <button onclick="calcSwap()" style="background:#2ecc71;color:white;border:none;padding:8px 20px;border-radius:6px;cursor:pointer;">Calculate</button>
                    </div>
                    <div id="calc-result" style="margin-top:12px;font-size:14px;color:#2c3e50;"></div>
                </div>

                <div class="table-container">
                    <h4 style="margin-bottom:12px;">Withdrawal Requests (WTC → HKD)</h4>
                    <table class="table">
                        <thead><tr><th>ID</th><th>User</th><th>HKD Amount</th><th>Status</th><th>Detail</th><th>Action</th></tr></thead>
                        <tbody id="swap-table-body"><tr><td colspan="6">Loading...</td></tr></tbody>
                    </table>
                </div>
            </div>

'''
c = c.replace(old_end, swap_html + old_end)
print("Swap section HTML added")

# 3. Add swap JS before </script>
swap_js = '''
        // === WTC/HKD Swap ===
        async function loadSwapData() {
            try { var r = await fetch('/admin/api/swap_rate'); var d = await r.json();
                document.getElementById('rate-wtc').value = d.wtc;
                document.getElementById('rate-hkd').value = d.hkd;
                document.getElementById('rate-fee').value = d.fee;
            } catch(e) {}
            try { var r = await fetch('/admin/api/swaps'); var swaps = await r.json();
                var tb = document.getElementById('swap-table-body');
                if (!tb) return;
                if (!swaps || swaps.length === 0) { tb.innerHTML = '<tr><td colspan="6">No requests</td></tr>'; return; }
                var html = '';
                for (var i = 0; i < swaps.length; i++) {
                    var s = swaps[i];
                    html += '<tr><td>' + (s.id||'') + '</td><td>' + (s.user||'') + '</td><td>HK$' + (s.amount||0) + '</td><td>' + (s.status||'Pending') + '</td>';
                    html += '<td style="font-size:11px;color:#64748b;">' + (s.detail||'-') + '</td>';
                    html += '<td>' + ((s.status||'Pending') === 'Pending'
                        ? '<button onclick="approveSwap(' + s.id + ",'approve')\" style=\"background:#27ae60;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;\">Approve</button> "
                        + '<button onclick="approveSwap(' + s.id + ",'reject')\" style=\"background:#e74c3c;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;\">Reject</button>'
                        : '<span style="color:#64748b;">Done</span>') + '</td></tr>';
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
            } catch(e) { document.getElementById('rate-status').textContent = 'Error: ' + e.message; }
            btn.disabled = false; btn.innerHTML = 'Update Rate';
            setTimeout(function(){ document.getElementById('rate-status').textContent = ''; }, 3000);
        }
        async function approveSwap(id, action) {
            try { var r = await fetch('/admin/api/approve_swap', { method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({id, action}) });
                var d = await r.json();
                if (d.success) loadSwapData();
            } catch(e) { alert('Error: ' + e.message); }
        }
        function calcSwap() {
            var wtc = parseFloat(document.getElementById('calc-wtc').value);
            if (!wtc || wtc <= 0) { document.getElementById('calc-result').textContent = ''; return; }
            var rw = parseInt(document.getElementById('rate-wtc').value);
            var rh = parseInt(document.getElementById('rate-hkd').value);
            var f = parseInt(document.getElementById('rate-fee').value);
            var g = wtc * rh / rw; var fa = g * f / 100; var n = g - fa;
            document.getElementById('calc-result').innerHTML =
                '<div style="background:#f0fdf4;padding:12px;border-radius:8px;"><b>' + wtc + ' WTC</b> &rarr; <b>HK$' + n.toFixed(2) + '</b><br>' +
                '<span style="font-size:12px;color:#64748b;">Gross: HK$' + g.toFixed(2) + ' | Fee (' + f + '%): HK$' + fa.toFixed(2) + '</span></div>';
        }
        // Add swap to showSection
        var origShow = showSection;
        showSection = function(id, el) { origShow(id, el); if (id === 'swap') setTimeout(loadSwapData, 100); };
'''

c = c.replace("</script>", swap_js + "\n</script>")
print("Swap JS added")

open(path, "w", encoding="utf-8").write(c)
print(f"Done - {len(c)} bytes")
