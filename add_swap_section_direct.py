"""Directly add swap section HTML to admin template"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# Check what's at the end before </div> and <script>
lines = c.split("\n")
# Find the audit section end and script start
for i, line in enumerate(lines):
    if '<div id="section-audit"' in line:
        audit_start = i
    if '<script>' in line:
        script_start = i
        break

print(f"Audit section ends around line {audit_start}, Script starts at line {script_start}")

# The swap section should be RIGHT BEFORE <script>
swap_section = """            <div id="section-swap" class="section">
                <div class="admin-header"><h2>WTC/HKD Swap Management</h2></div>
                <div class="stat-card">
                    <h4>Exchange Rate</h4>
                    <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:12px;">
                        <div><label>WTC</label><input type="number" id="rate-wtc" value="10" style="width:80px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;"></div>
                        <span>=</span>
                        <div><label>HKD</label><input type="number" id="rate-hkd" value="1" style="width:80px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;"></div>
                        <div><label>Fee %</label><input type="number" id="rate-fee" value="10" style="width:80px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;"></div>
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
                    <h4>Withdrawal Requests (WTC to HKD)</h4>
                    <table class="table">
                        <thead><tr><th>ID</th><th>User</th><th>HKD Amount</th><th>Status</th><th>Detail</th><th>Action</th></tr></thead>
                        <tbody id="swap-table-body"><tr><td colspan="6">Loading...</td></tr></tbody>
                    </table>
                </div>
            </div>

"""

# Insert before <script>
c = c.replace("<script>", swap_section + "<script>")
open(path, "w", encoding="utf-8").write(c)
print(f"Swap section added. File: {len(c)} bytes")

# Verify
if "section-swap" in c:
    print("OK - section-swap exists")
