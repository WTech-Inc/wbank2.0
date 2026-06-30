"""Fix swap section alignment - use simpler layout"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# Replace the rate control row with a simpler flex layout
old_rate = """            <div class="row mb-3">
                <div class="col-md-1">
                    <label style="font-size:11px;color:#64748b;">WTC</label>
                    <input type="number" class="form-control form-control-sm" id="rate-wtc" value="10">
                </div>
                <div class="col-md-1" style="display:flex;align-items:end;justify-content:center;padding-bottom:8px;">
                    <span style="font-size:18px;">=</span>
                </div>
                <div class="col-md-1">
                    <label style="font-size:11px;color:#64748b;">HKD</label>
                    <input type="number" class="form-control form-control-sm" id="rate-hkd" value="1">
                </div>
                <div class="col-md-1">
                    <label style="font-size:11px;color:#64748b;">Fee %</label>
                    <input type="number" class="form-control form-control-sm" id="rate-fee" value="10">
                </div>
                <div class="col-md-2" style="display:flex;align-items:end;padding-bottom:8px;">
                    <button class="btn btn-primary btn-sm" onclick="updateSwapRate()">Update</button>
                    <span id="rate-status" style="font-size:12px;color:#27ae60;margin-left:8px;"></span>
                </div>
            </div>"""

new_rate = """            <div style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;">
                <div><label style="font-size:11px;color:#64748b;display:block;">WTC</label>
                    <input type="number" class="form-control form-control-sm" id="rate-wtc" value="10" style="width:70px;"></div>
                <div style="padding-bottom:8px;"><span style="font-size:18px;">=</span></div>
                <div><label style="font-size:11px;color:#64748b;display:block;">HKD</label>
                    <input type="number" class="form-control form-control-sm" id="rate-hkd" value="1" style="width:70px;"></div>
                <div><label style="font-size:11px;color:#64748b;display:block;">Fee %</label>
                    <input type="number" class="form-control form-control-sm" id="rate-fee" value="10" style="width:70px;"></div>
                <div style="padding-bottom:8px;">
                    <button class="btn btn-primary btn-sm" onclick="updateSwapRate()">Update</button>
                    <span id="rate-status" style="font-size:12px;color:#27ae60;margin-left:8px;"></span>
                </div>
            </div>"""

c = c.replace(old_rate, new_rate)

# Also fix calculator
old_calc = """            <div class="row mb-3">
                <div class="col-md-2">
                    <input type="number" class="form-control form-control-sm" id="calc-wtc" placeholder="WTC">
                </div>
                <div class="col-md-2">
                    <button class="btn btn-success btn-sm" onclick="calcSwap()">Calculate</button>
                </div>
            </div>"""

new_calc = """            <div style="display:flex;gap:12px;align-items:center;">
                <div><input type="number" class="form-control form-control-sm" id="calc-wtc" placeholder="WTC amount" style="width:150px;"></div>
                <div><button class="btn btn-success btn-sm" onclick="calcSwap()">Calculate</button></div>
            </div>"""

c = c.replace(old_calc, new_calc)

open(path, "w", encoding="utf-8").write(c)
print(f"Done - {len(c)} bytes")
