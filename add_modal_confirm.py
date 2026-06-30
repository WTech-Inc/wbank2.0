"""Add modal confirmation for approve - shows HKD amount"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/main.py", "r", encoding="utf-8").read()

# Find the rows_html generation and add data-amount attribute to approve forms
old_row_start = "rows_html += '<td>'"
new_row_start = """        # Add data attributes for modal
        row_amount = str(r['amount'] or 0)
        row_detail = (r['detail'] or '')"""

c = c.replace(old_row_start, new_row_start)

# Update the approve button to include data attributes
old_approve_btn = """rows_html += '<button class="btn btn-success btn-sm" type="submit">Approve</button>'"""
new_approve_btn = """rows_html += '<button class="btn btn-success btn-sm" type="button" onclick="showApprove('+str(r['id'])+',\\''+row_amount+'\\')">Approve</button>'"""

c = c.replace(old_approve_btn, new_approve_btn)

# Add modal HTML and JS after the table
old_table_end = """html += '</tbody></table></div></div>'"""
new_table_end = """html += '</tbody></table></div></div>

<div class="modal fade" id="approveModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Confirm Withdrawal</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <p>User will receive: <strong id="modal-amount">HK$0</strong> in cash</p>
        <p id="modal-detail" style="font-size:12px;color:#64748b;"></p>
      </div>
      <div class="modal-footer">
        <form id="approve-form" method="POST" action="/admin/api/approve_swap">
          <input type="hidden" name="id" id="modal-id" value="">
          <input type="hidden" name="action" value="approve">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn btn-success">Confirm & Approve</button>
        </form>
      </div>
    </div>
  </div>
</div>

<script>
function showApprove(id, amount) {
  document.getElementById("modal-id").value = id;
  document.getElementById("modal-amount").textContent = "HK$" + amount;
  var modal = new bootstrap.Modal(document.getElementById("approveModal"));
  modal.show();
}
</script>'''

c = c.replace(old_table_end, new_table_end)

open("E:/wbank/main.py", "w", encoding="utf-8").write(c)
print("OK")
