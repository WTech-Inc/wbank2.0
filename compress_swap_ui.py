"""Compress swap section UI to fit better"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# Make rate controls more compact: col-md-2 -> col-md-1, col-md-3 -> col-md-2
c = c.replace('class="col-md-2">\n                    <label style="font-size:12px;color:#64748b;">WTC</label>',
              'class="col-md-1">\n                    <label style="font-size:11px;color:#64748b;">WTC</label>')

c = c.replace('class="col-md-2">\n                    <label style="font-size:12px;color:#64748b;">HKD</label>',
              'class="col-md-1">\n                    <label style="font-size:11px;color:#64748b;">HKD</label>')

c = c.replace('class="col-md-2">\n                    <label style="font-size:12px;color:#64748b;">Fee %</label>',
              'class="col-md-1">\n                    <label style="font-size:11px;color:#64748b;">Fee %</label>')

c = c.replace('class="col-md-3" style="display:flex;align-items:end;padding-bottom:8px;">\n                    <button class="btn btn-primary btn-sm" onclick="updateSwapRate()">Update</button>',
              'class="col-md-2" style="display:flex;align-items:end;padding-bottom:8px;">\n                    <button class="btn btn-primary btn-sm" onclick="updateSwapRate()">Update</button>')

# Make calculator more compact
c = c.replace('class="col-md-3">\n                    <input type="number" class="form-control form-control-sm" id="calc-wtc" placeholder="WTC amount">',
              'class="col-md-2">\n                    <input type="number" class="form-control form-control-sm" id="calc-wtc" placeholder="WTC">')

open(path, "w", encoding="utf-8").write(c)
print(f"Done - {len(c)} bytes")
