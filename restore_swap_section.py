"""Restore swap section HTML in admin template"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

if "section-swap" in c:
    print("Swap section already exists")
    sys.exit(0)

# Find the audit section end and insert swap section before it
swap_section = """            <div id="section-swap" class="section">
                <div class="admin-header"><h2>WTC/HKD Swap Management</h2></div>

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
                    <h4>Swap Calculator</h4>
                    <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:12px;">
                        <input type="number" id="calc-wtc" placeholder="WTC amount" style="width:200px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;">
                        <button onclick="calcSwap()" style="background:#2ecc71;color:white;border:none;padding:8px 20px;border-radius:6px;cursor:pointer;">Calculate</button>
                    </div>
                    <div id="calc-result" style="margin-top:12px;font-size:14px;color:#2c3e50;"></div>
                </div>

                <div class="table-container">
                    <h4 style="margin-bottom:12px;">Withdrawal Requests (WTC -> HKD)</h4>
                    <table class="table">
                        <thead><tr><th>ID</th><th>User</th><th>HKD Amount</th><th>Status</th><th>Conversion Detail</th><th>Action</th></tr></thead>
                        <tbody id="swap-table-body"><tr><td colspan="6">Loading...</td></tr></tbody>
                    </table>
                </div>
            </div>

"""

# Insert before the last </div> of content section + script
insert_before = '        // === WTC/HKD Swap ==='
if insert_before in c:
    c = c.replace(insert_before, swap_section + "\n        " + insert_before)
    open(path, "w", encoding="utf-8").write(c)
    print("OK - swap section restored")
else:
    print(f"Marker '{insert_before}' not found")
    # Try finding script end
    idx = c.rfind("</script>")
    if idx > 0:
        c = c[:idx] + swap_section + "\n    <script>\n" + c[idx:]
        open(path, "w", encoding="utf-8").write(c)
        print("OK - swap section added before last script")
