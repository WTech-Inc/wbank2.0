"""Add swap to admin - using template literals to avoid quote issues"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8").read()

# 1. Sidebar link - simple text, no emoji
c = c.replace(
    'showSection(\'audit\', this)">',
    'showSection(\'audit\', this)">\n        <a href="#" onclick="showSection(\'swap\', this)">SWAP</a>'
)

# Hmm that won't work as expected. Let me be more precise.
# Find the exact audit link end and add swap after it

idx = c.find("showSection('kyc', this)")
link_end = c.find("</a>", idx)
swap_link = '\n        <a href="#" onclick="showSection(\'swap\', this)">SWAP</a>'
c = c[:link_end+4] + swap_link + c[link_end+4:]

# 2. Swap section HTML
swap_section = """
    <div id="section-swap" class="section">
        <div class="table-container">
            <h4>WTC/HKD Swap Requests</h4>
            <table class="table table-striped">
                <thead><tr><th>ID</th><th>User</th><th>HKD</th><th>Status</th><th>Detail</th><th>Action</th></tr></thead>
                <tbody id="swap-tb"><tr><td colspan="6">Loading...</td></tr></tbody>
            </table>
        </div>
    </div>
"""
c = c.replace("<script>", swap_section + "\n<script>")

# 3. Swap JS using template literals (backticks) - no quote issues
swap_js = """
function loadSwap() {
    fetch('/admin/api/swaps').then(function(r){return r.json()}).then(function(rows){
        var tb = document.getElementById('swap-tb');
        if (!tb) return;
        if (!rows || rows.length === 0) { tb.innerHTML = '<tr><td colspan=\"6\">None</td></tr>'; return; }
        var h = '';
        for (var i = 0; i < rows.length; i++) {
            var r = rows[i];
            var st = r.status || 'Pending';
            h += '<tr>';
            h += '<td>' + r.id + '</td>';
            h += '<td>' + r.user + '</td>';
            h += '<td>HK$' + (r.amount || 0) + '</td>';
            h += '<td>' + st + '</td>';
            h += '<td>' + (r.detail || '-') + '</td>';
            h += '<td>';
            if (st === 'Pending') {
                h += '<span style=\"color:#27ae60;cursor:pointer\" onclick=\"doApprove(' + r.id + ",'approve')\">[Approve]</span> ";
                h += '<span style=\"color:#e74c3c;cursor:pointer\" onclick=\"doApprove(' + r.id + ",'reject')\">[Reject]</span>";
            } else {
                h += '<span style=\"color:#64748b\">Done</span>';
            }
            h += '</td></tr>';
        }
        tb.innerHTML = h;
    }).catch(function(e){console.log(e);});
}
function doApprove(id, action) {
    if (action === 'approve' && !confirm('Approve this withdrawal?')) return;
    fetch('/admin/api/approve_swap', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:id,action:action})})
    .then(function(r){return r.json()}).then(function(d){if(d.success)loadSwap();}).catch(function(e){alert(e.message);});
}
var os = showSection;
showSection = function(id,el){os(id,el);if(id==='swap')setTimeout(loadSwap,100);};
"""

c = c.replace("</script>", swap_js + "\n</script>")

open("E:/wbank/templates/admin/index.html", "w", encoding="utf-8").write(c)
print(f"Done ({len(c)} bytes)")
