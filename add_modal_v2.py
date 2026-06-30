"""Add modal confirmation for approve"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/main.py", "r", encoding="utf-8").read()

# 1. Add data attributes to rows
old1 = "rows_html += '<td>' + str(r['id']) + '</td>'"
new1 = "rows_html += '<td>' + str(r['id']) + '</td>'\n        row_amt = str(r['amount'] or 0)"
c = c.replace(old1, new1)

# 2. Update approve button to call showApprove modal
old2 = """rows_html += '<button class="btn btn-success btn-sm" type="submit">Approve</button>'"""
new2 = """rows_html += '<button class="btn btn-success btn-sm" type="button" onclick=\\'showApprove('+str(r['id'])+',\\\"'+str(r['amount'] or 0)+'\\\")\\'>Approve</button>'"""
c = c.replace(old2, new2)

# 3. Add modal and JS before </body></html>
old3 = "html += '</body></html>'"
new3 = """html += '''
<div class="modal" id="appModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header"><h5>Confirm Withdrawal</h5><button type="button" class="btn-close" onclick="document.getElementById('appModal').style.display='none'"></button></div>
      <div class="modal-body">
        <p>User receives: HK$<strong id="mAmt">0</strong> in cash</p>
      </div>
      <div class="modal-footer">
        <form id="mForm" method="POST" action="/admin/api/approve_swap">
          <input type="hidden" name="id" id="mId" value="">
          <input type="hidden" name="action" value="approve">
          <button type="button" class="btn btn-secondary" onclick="document.getElementById('appModal').style.display='none'">Cancel</button>
          <button type="submit" class="btn btn-success">Confirm</button>
        </form>
      </div>
    </div>
  </div>
</div>
<style>.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:9999}.modal-dialog{background:white;margin:100px auto;max-width:400px;border-radius:8px;overflow:hidden}.modal-header{padding:15px;border-bottom:1px solid #e2e8f0;font-weight:bold}.modal-body{padding:15px}.modal-footer{padding:15px;border-top:1px solid #e2e8f0;text-align:right}.btn-close{float:right;border:none;background:none;font-size:20px;cursor:pointer}.modal.show{display:block}</style>
<script>
function showApprove(id, amt) {
  document.getElementById("mId").value = id;
  document.getElementById("mAmt").textContent = amt;
  document.getElementById("appModal").classList.add("show");
}
document.getElementById("appModal").addEventListener("click", function(e) {
  if (e.target === this) this.classList.remove("show");
});
</script>
''' + chr(10) + "html += '</body></html>'"

c = c.replace(old3, new3)

# Verify syntax
import py_compile
import os
with open("E:/wbank/main.py.tmp", "w", encoding="utf-8") as f:
    f.write(c)
try:
    py_compile.compile("E:/wbank/main.py.tmp", doraise=True)
    os.replace("E:/wbank/main.py.tmp", "E:/wbank/main.py")
    print("OK - modal added, syntax verified")
except Exception as e:
    print(f"SYNTAX ERROR: {e}")
