"""Rebuild swap section to use admin theme classes"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# Find the swap section and replace it
old_start = '    <div id="section-swap" class="section">'
old_end = '            </div>\n\n        </div>'

# Find where the swap section starts and ends
lines = c.split("\n")
swap_start = -1
swap_end = -1
for i, line in enumerate(lines):
    if 'id="section-swap"' in line:
        swap_start = i
    if swap_start >= 0 and i > swap_start and line.strip().startswith("// ===") and "Swap" in line:
        swap_end = i
        break

if swap_start < 0:
    print("Swap section not found!")
    sys.exit(1)

print(f"Swap section: lines {swap_start+1} to {swap_end+1}")

# Build new swap section
new_swap = """    <div id="section-swap" class="section">
        <div class="stat-card">
            <h4>Exchange Rate</h4>
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
                    <button class="btn btn-primary btn-sm" onclick="updateSwapRate()">Update Rate</button>
                    &nbsp;<span id="rate-status" style="font-size:12px;color:#27ae60;"></span>
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
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>User</th>
                            <th>HKD</th>
                            <th>Status</th>
                            <th>Detail</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody id="swap-table-body">
                        <tr><td colspan="6" class="loading">Loading...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>"""

# Replace old swap section with new one
old_content = "\n".join(lines[swap_start:swap_end])
c = c.replace(old_content, new_swap)

open(path, "w", encoding="utf-8").write(c)
print(f"Done - swap section rebuilt ({len(c)} bytes)")
