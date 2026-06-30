"""Add confirm() dialog to approve buttons"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/main.py", "r", encoding="utf-8").read()

# Remove old modal attempt
c = c.replace('''<div class="modal" id="appModal" tabindex="-1">
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
''', "")

# Add confirm() to approve buttons
old_btn = '<button class="btn btn-success btn-sm" type="button" onclick=\'showApprove('
new_btn = '<button class="btn btn-success btn-sm" type="submit" onclick=\'return confirm("Confirm this withdrawal? HK$'

if old_btn in c:
    c = c.replace(old_btn, new_btn)
    # Also fix the end of the onclick
    c = c.replace(")\\'>Approve</button>'", ")\")'>Approve</button>'")
    print("Confirm added to approve buttons")
else:
    print("Pattern not found. Checking...")
    idx = c.find("btn-success btn-sm")
    if idx >= 0:
        print(f"Found button at {idx}: {c[idx:idx+80]}")

open("E:/wbank/main.py", "w", encoding="utf-8").write(c)
print(f"Saved ({len(c)} bytes)")
