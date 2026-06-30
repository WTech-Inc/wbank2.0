"""Add swap section with minimal, clean JS - no complex quoting"""
import sys, json
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# 1. Add swap link after Audit
c = c.replace(
    'showSection(\'audit\', this)">',
    'showSection(\'audit\', this)">\n        <a href="#" onclick="showSection(\'swap\', this)">SWAP</a>'
)
# Actually the above is wrong - let me find the exact KYC link
idx = c.find("showSection('kyc', this)")
link_end = c.find("</a>", idx)
swap_link = '\n        <a href="#" onclick="showSection(\'swap\', this)">SWAP</a>'
c = c[:link_end+4] + swap_link + c[link_end+4:]

# 2. Add swap section HTML (before script) - very simple
swap_html = """
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
c = c.replace("<script>", swap_html + "\n<script>")

# 3. Add swap JS (before </script>) - minimal, clean
swap_js = """
function loadSwapData() {
    fetch('/admin/api/swaps').then(function(r){return r.json()}).then(function(swaps){
        var tb = document.getElementById('swap-tb');
        if (!tb) return;
        if (!swaps || swaps.length === 0) { tb.innerHTML = '<tr><td colspan=\"6\">None</td></tr>'; return; }
        var html = '';
        for (var i = 0; i < swaps.length; i++) {
            var s = swaps[i];
            var st = s.status || 'Pending';
            html += '<tr><td>'+(s.id||'')+'</td><td>'+(s.user||'')+'</td><td>HK$'+(s.amount||0)+'</td><td>'+st+'</td>';
            html += '<td>'+(s.detail||'-')+'</td><td>';
            if (st === 'Pending') {
                html += '<span style=\"color:#27ae60;cursor:pointer;\" onclick=\"doApprove('+s.id+',\\'approve\\')\">[Approve]</span> ';
                html += '<span style=\"color:#e74c3c;cursor:pointer;\" onclick=\"doApprove('+s.id+',\\'reject\\')\">[Reject]</span>';
            } else {
                html += '<span style=\"color:#64748b;\">Done</span>';
            }
            html += '</td></tr>';
        }
        tb.innerHTML = html;
    }).catch(function(e){console.log(e);});
}
function doApprove(id, action) {
    if (action === 'approve' && !confirm('Confirm this withdrawal?')) return;
    fetch('/admin/api/approve_swap', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:id,action:action})})
    .then(function(r){return r.json()}).then(function(d){if(d.success)loadSwapData();}).catch(function(e){alert(e.message);});
}
var orig = showSection;
showSection = function(id,el){orig(id,el);if(id==='swap')setTimeout(loadSwapData,100);};
"""

c = c.replace("</script>", swap_js + "\n</script>")

open(path, "w", encoding="utf-8").write(c)
print(f"Done ({len(c)} bytes)")
