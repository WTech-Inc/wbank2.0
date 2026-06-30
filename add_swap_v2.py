"""
WTC/HKD Swap System - WBank Internal Exchange
Rate: 10 WTC = 1 HKD
Fee: 10%
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

MAIN = "E:/wbank/main.py"
TPL = "E:/wbank/templates/admin/index.html"
CLIENT_TPL = "E:/wbank/templates/wbankClient.html"

# ═══ 1. Add config table to models.py ═══
models = open("E:/wbank/models.py", "r", encoding="utf-8").read()

# Add swap_config model if not exists
if "class swap_config" not in models:
    swap_model = '''

class swap_config(db.Model):
    __tablename__ = 'swap_config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rate_wtc = db.Column(db.Integer, default=10)
    rate_hkd = db.Column(db.Integer, default=1)
    fee_percent = db.Column(db.Integer, default=10)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, rate_wtc=10, rate_hkd=1, fee_percent=10):
        self.rate_wtc = rate_wtc
        self.rate_hkd = rate_hkd
        self.fee_percent = fee_percent
        self.updated_at = datetime.datetime.utcnow()
'''
    models += swap_model
    open("E:/wbank/models.py", "w", encoding="utf-8").write(models)
    print("[OK] swap_config model added")
else:
    print("[OK] swap_config already exists")

# ═══ 2. Add routes to main.py ═══
main = open(MAIN, "r", encoding="utf-8").read()

# User routes
swap_user_routes = '''

@app.route("/wbank/swap/info", methods=["GET"])
def wbank_swap_info():
    """Get current exchange rate and fee"""
    rate = swap_config.query.first()
    wtc_rate = rate.rate_wtc if rate else 10
    hkd_rate = rate.rate_hkd if rate else 1
    fee = rate.fee_percent if rate else 10
    return jsonify({
        "wtc": wtc_rate,
        "hkd": hkd_rate,
        "fee_percent": fee,
        "rate_label": f"{wtc_rate} WTC = {hkd_rate} HKD",
        "fee_label": f"{fee}% handling fee"
    })

@app.route("/wbank/swap/apply", methods=["POST"])
@login_required
def wbank_swap_apply():
    """User applies to swap WTC to HKD"""
    user = current_user.username
    wtc_amount = int(request.json.get("amount", 0))
    if wtc_amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    user_data = wbankwallet.query.filter_by(username=user).first()
    if not user_data or int(user_data.balance) < wtc_amount:
        return jsonify({"error": "Insufficient WTC balance"}), 400

    rate = swap_config.query.first()
    wtc_rate = rate.rate_wtc if rate else 10
    hkd_rate = rate.rate_hkd if rate else 1
    fee_pct = rate.fee_percent if rate else 10

    gross_hkd = wtc_amount * hkd_rate / wtc_rate
    fee_amount = gross_hkd * fee_pct / 100
    net_hkd = gross_hkd - fee_amount

    # Deduct WTC from user balance
    user_data.balance = str(int(user_data.balance) - wtc_amount)

    # Create swap record (using cashout table)
    new_swap = cashout(name=user, amount=round(net_hkd, 2))
    db.session.add(new_swap)
    db.session.commit()

    from main import log_audit
    log_audit("SWAP_APPLY", user, f"Swapped {wtc_amount} WTC -> {round(net_hkd,2)} HKD (Fee: {round(fee_amount,2)} HKD)")

    return jsonify({
        "success": True,
        "wtc_amount": wtc_amount,
        "gross_hkd": round(gross_hkd, 2),
        "fee_hkd": round(fee_amount, 2),
        "net_hkd": round(net_hkd, 2),
        "rate": f"{wtc_rate} WTC = {hkd_rate} HKD"
    })

'''

# Admin routes
swap_admin_routes = '''

@app.route("/admin/api/swap_rate", methods=["GET", "POST"])
@csrf.exempt
def admin_swap_rate():
    """Admin: Get or set swap rate"""
    if request.method == "POST":
        data = request.json
        rate = swap_config.query.first()
        if not rate:
            rate = swap_config()
            db.session.add(rate)

        if "wtc" in data:
            rate.rate_wtc = int(data["wtc"])
        if "hkd" in data:
            rate.rate_hkd = int(data["hkd"])
        if "fee" in data:
            rate.fee_percent = int(data["fee"])
        rate.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        return jsonify({"success": True, "message": "Rate updated"})

    rate = swap_config.query.first()
    return jsonify({
        "wtc": rate.rate_wtc if rate else 10,
        "hkd": rate.rate_hkd if rate else 1,
        "fee": rate.fee_percent if rate else 10
    })

@app.route("/admin/api/swaps")
@csrf.exempt
def admin_api_swaps():
    """Admin: Get all swap requests"""
    swaps = cashout.query.order_by(cashout.id.desc()).all()
    return jsonify([{
        "id": s.id,
        "user": s.name,
        "amount": s.amount,
        "status": s.status,
    } for s in swaps])

@app.route("/admin/api/approve_swap", methods=["POST"])
@csrf.exempt
def admin_approve_swap():
    """Admin: Approve or reject swap"""
    data = request.json
    swap_id = data.get("id")
    action = data.get("action", "approve")

    record = cashout.query.get(swap_id)
    if not record:
        return jsonify({"error": "Swap not found"}), 404

    if action == "approve":
        record.status = "已批准 Approved"
    elif action == "reject":
        record.status = "已拒絕 Rejected"

    db.session.commit()
    return jsonify({"success": True, "status": record.status})

'''

# Insert routes into main.py
# Find a good insertion point - before the cashout routes
if "def wbank_swap_info" not in main:
    insert_point = main.find("@app.route(\"/wbank/v1/cashout\")")
    if insert_point >= 0:
        main = main[:insert_point] + swap_user_routes + main[insert_point:]
        print("[OK] User swap routes added")
    else:
        print("[ERROR] Could not find insertion point for user routes")

    insert_point2 = main.find("@app.route(\"/admin/api/audit_log\")")
    if insert_point2 >= 0:
        end_of_audit = main.find("\n@", insert_point2 + 50)
        if end_of_audit > 0:
            main = main[:end_of_audit] + swap_admin_routes + main[end_of_audit:]
            print("[OK] Admin swap routes added")
else:
    print("[OK] Swap routes already exist")

open(MAIN, "w", encoding="utf-8").write(main)

# ═══ 3. Add Admin Panel UI tab ═══
admin_tpl = open(TPL, "r", encoding="utf-8").read()

# Add Swap section to admin sidebar
sidebar_item = '<a href="#" onclick="showSection(\'swap\')">💱 WTC/HKD Swap</a>'
if sidebar_item not in admin_tpl:
    insert_after = '<a href="#" onclick="showSection(\'audit\')">📋 Audit Log</a>'
    admin_tpl = admin_tpl.replace(insert_after, insert_after + "\n        " + sidebar_item)

# Add Swap section HTML (before closing </div> of content)
swap_section = '''
            <div id="section-swap" class="section">
                <div class="admin-header">
                    <h2>💱 WTC/HKD Swap Management</h2>
                </div>

                <div class="stat-card">
                    <h4>Exchange Rate</h4>
                    <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:12px;">
                        <div>
                            <label style="font-size:12px;color:#64748b;">WTC</label>
                            <input type="number" id="rate-wtc" value="10" style="width:80px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;">
                        </div>
                        <span style="font-size:18px;">=</span>
                        <div>
                            <label style="font-size:12px;color:#64748b;">HKD</label>
                            <input type="number" id="rate-hkd" value="1" style="width:80px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;">
                        </div>
                        <div>
                            <label style="font-size:12px;color:#64748b;">Fee %</label>
                            <input type="number" id="rate-fee" value="10" style="width:80px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;">
                        </div>
                        <button onclick="updateSwapRate()" style="background:#3498db;color:white;border:none;padding:8px 20px;border-radius:6px;cursor:pointer;">Update Rate</button>
                        <span id="rate-status" style="font-size:12px;color:#27ae60;"></span>
                    </div>
                </div>

                <div class="stat-card">
                    <h4>Swap Calculator</h4>
                    <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:12px;">
                        <input type="number" id="calc-wtc" placeholder="Enter WTC amount" style="width:200px;padding:8px;border:1px solid #e2e8f0;border-radius:6px;">
                        <button onclick="calcSwap()" style="background:#2ecc71;color:white;border:none;padding:8px 20px;border-radius:6px;cursor:pointer;">Calculate</button>
                    </div>
                    <div id="calc-result" style="margin-top:12px;font-size:14px;color:#2c3e50;"></div>
                </div>

                <div class="table-container">
                    <h4 style="margin-bottom:12px;">Swap Requests</h4>
                    <table class="table">
                        <thead><tr><th>ID</th><th>User</th><th>Amount (HKD)</th><th>Status</th><th>Action</th></tr></thead>
                        <tbody id="swap-table-body"><tr><td colspan="5">Loading...</td></tr></tbody>
                    </table>
                </div>
            </div>
'''

if "section-swap" not in admin_tpl:
    admin_tpl = admin_tpl.replace('</div>\n\n    <script>', swap_section + '\n    <script>')

# Add JS functions
swap_js = '''
        // === WTC/HKD Swap ===
        function showSection(name) {
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            document.getElementById('section-' + name).classList.add('active');
            document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
            const link = document.querySelector(`.sidebar a[onclick*="'${name}'"]`);
            if (link) link.classList.add('active');
            if (name === 'swap') loadSwapData();
        }

        async function loadSwapData() {
            try {
                const r = await fetch('/admin/api/swap_rate');
                const d = await r.json();
                document.getElementById('rate-wtc').value = d.wtc;
                document.getElementById('rate-hkd').value = d.hkd;
                document.getElementById('rate-fee').value = d.fee;
            } catch(e) {}
            try {
                const r = await fetch('/admin/api/swaps');
                const swaps = await r.json();
                const tbody = document.getElementById('swap-table-body');
                if (!swaps || swaps.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="5">No swap requests</td></tr>';
                    return;
                }
                tbody.innerHTML = swaps.map(s =>
                    '<tr><td>' + s.id + '</td><td>' + s.user + '</td><td>HK$' + s.amount + '</td><td>' + (s.status || 'Pending') + '</td>' +
                    '<td>' + ((s.status || 'Pending') === 'Pending' ?
                        '<button onclick="approveSwap(' + s.id + ',\\'approve\\')" style="background:#27ae60;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;">Approve</button> ' +
                        '<button onclick="approveSwap(' + s.id + ',\\'reject\\')" style="background:#e74c3c;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;">Reject</button>'
                        : '<span style="color:#64748b;">Done</span>') +
                    '</td></tr>'
                ).join('');
            } catch(e) { console.log('Swap:', e); }
        }

        async function updateSwapRate() {
            const btn = event.target;
            btn.disabled = true;
            btn.innerHTML = 'Saving...';
            try {
                const r = await fetch('/admin/api/swap_rate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        wtc: parseInt(document.getElementById('rate-wtc').value),
                        hkd: parseInt(document.getElementById('rate-hkd').value),
                        fee: parseInt(document.getElementById('rate-fee').value)
                    })
                });
                const d = await r.json();
                document.getElementById('rate-status').textContent = d.success ? 'Updated!' : 'Error';
            } catch(e) {
                document.getElementById('rate-status').textContent = 'Error: ' + e.message;
            }
            btn.disabled = false;
            btn.innerHTML = 'Update Rate';
            setTimeout(() => document.getElementById('rate-status').textContent = '', 3000);
        }

        async function approveSwap(id, action) {
            try {
                const r = await fetch('/admin/api/approve_swap', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({id, action})
                });
                const d = await r.json();
                if (d.success) loadSwapData();
            } catch(e) { alert('Error: ' + e.message); }
        }

        function calcSwap() {
            const wtc = parseFloat(document.getElementById('calc-wtc').value);
            if (!wtc || wtc <= 0) { document.getElementById('calc-result').textContent = ''; return; }
            const rateWtc = parseInt(document.getElementById('rate-wtc').value);
            const rateHkd = parseInt(document.getElementById('rate-hkd').value);
            const fee = parseInt(document.getElementById('rate-fee').value);
            const grossHkd = wtc * rateHkd / rateWtc;
            const feeAmount = grossHkd * fee / 100;
            const netHkd = grossHkd - feeAmount;
            document.getElementById('calc-result').innerHTML =
                '<div style="background:#f0fdf4;padding:12px;border-radius:8px;">' +
                '<b>' + wtc + ' WTC</b> → <b>HK$' + netHkd.toFixed(2) + '</b><br>' +
                '<span style="font-size:12px;color:#64748b;">Gross: HK$' + grossHkd.toFixed(2) +
                ' | Fee (' + fee + '%): HK$' + feeAmount.toFixed(2) + '</span></div>';
        }
'''

if "function loadSwapData" not in admin_tpl:
    admin_tpl = admin_tpl.replace('</script>', swap_js + '\n</script>')

open(TPL, "w", encoding="utf-8").write(admin_tpl)
print("[OK] Admin panel UI updated")

# ═══ 4. Add User Panel UI to wbankClient.html ═══
client = open(CLIENT_TPL, "r", encoding="utf-8").read()

# Add Swap nav item
swap_nav = '<div class="nav-item" onclick="showPage(\'swap\')">💱<br>Swap</div>'
if "showPage('swap')" not in client:
    client = client.replace(
        '<div class="nav-item" onclick="showPage(\'web3\')">🔗<br>Web3</div>',
        '<div class="nav-item" onclick="showPage(\'web3\')">🔗<br>Web3</div>\n        <div class="nav-item" onclick="showPage(\'swap\')">💱<br>Swap</div>'
    )

# Add Swap page HTML (before closing </div> of main-content)
swap_page = '''
        <div id="swap" class="page">
            <div class="card">
                <div style="font-size:32px;margin-bottom:8px;">💱</div>
                <h2 style="color:#1a1a2e;">WTC/HKD Swap</h2>
                <p style="font-size:13px;color:#94a3b8;">Convert your WTC to HKD digital cash</p>
            </div>

            <div class="balance-card" style="background:linear-gradient(135deg,#059669,#10b981);">
                <div class="label">Exchange Rate</div>
                <div class="balance" style="font-size:24px;"><span id="swap-rate-display">Loading...</span></div>
                <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:4px;">Fee: <span id="swap-fee-display">10%</span></div>
            </div>

            <div class="card">
                <h3>Swap WTC → HKD</h3>
                <div style="margin-bottom:8px;">
                    <label style="font-size:13px;color:#64748b;">WTC Amount</label>
                    <input type="number" id="swap-amount" placeholder="Enter WTC amount" oninput="updateSwapPreview()">
                </div>
                <div id="swap-preview" style="display:none;background:#f0fdf4;padding:12px;border-radius:8px;margin-bottom:12px;">
                    <div style="font-size:13px;color:#059669;">You will receive:</div>
                    <div style="font-size:24px;font-weight:700;color:#059669;">HK$ <span id="swap-net"></span></div>
                    <div style="font-size:12px;color:#64748b;margin-top:4px;">
                        Gross: HK$ <span id="swap-gross"></span>
                        | Fee (<span id="swap-fee-pct"></span>%): HK$ <span id="swap-fee"></span>
                    </div>
                </div>
                <button class="btn btn-primary" onclick="applySwap()" id="swap-btn" disabled>Apply Swap</button>
                <div id="swap-result" style="margin-top:12px;display:none;"></div>
            </div>

            <div class="card">
                <h3>Swap History</h3>
                <div id="swap-history" style="font-size:13px;color:#94a3b8;">Loading...</div>
            </div>
        </div>
'''

if "id=\"swap\"" not in client:
    client = client.replace('</div>\n\n    <div class="nav-bar">', swap_page + '\n    </div>\n\n    <div class="nav-bar">')

# Add Swap JS
swap_client_js = '''
        // === WTC/HKD Swap ===
        let swapRate = {wtc: 10, hkd: 1, fee: 10};

        async function loadSwapInfo() {
            try {
                const r = await fetch('/wbank/swap/info');
                const d = await r.json();
                swapRate = d;
                document.getElementById('swap-rate-display').textContent = d.rate_label;
                document.getElementById('swap-fee-display').textContent = d.fee_label;
                document.getElementById('swap-fee-pct').textContent = d.fee_percent;
            } catch(e) {
                document.getElementById('swap-rate-display').textContent = '10 WTC = 1 HKD';
            }
            try {
                const r = await fetch('/wbank/web3/history');
                const txns = await r.json();
                const swaps = txns.filter(t => t.action && t.action.indexOf('SWAP') >= 0);
                const container = document.getElementById('swap-history');
                if (!swaps || swaps.length === 0) {
                    container.innerHTML = '<p style="text-align:center;padding:20px;">No swap history</p>';
                } else {
                    container.innerHTML = swaps.map(t =>
                        '<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">' +
                        '<span style="color:#1a1a2e;">' + (t.action || '') + '</span><br>' +
                        '<span style="color:#94a3b8;">' + (t.time || '') + '</span></div>'
                    ).join('');
                }
            } catch(e) { console.log('Swap history:', e); }
        }

        function updateSwapPreview() {
            const amt = parseFloat(document.getElementById('swap-amount').value);
            const preview = document.getElementById('swap-preview');
            const btn = document.getElementById('swap-btn');
            if (!amt || amt <= 0) {
                preview.style.display = 'none';
                btn.disabled = true;
                return;
            }
            const gross = amt * swapRate.hkd / swapRate.wtc;
            const fee = gross * swapRate.fee / 100;
            const net = gross - fee;
            document.getElementById('swap-gross').textContent = gross.toFixed(2);
            document.getElementById('swap-fee').textContent = fee.toFixed(2);
            document.getElementById('swap-net').textContent = net.toFixed(2);
            preview.style.display = 'block';
            btn.disabled = false;
        }

        async function applySwap() {
            const amt = parseInt(document.getElementById('swap-amount').value);
            if (!amt || amt <= 0) return;
            const btn = document.getElementById('swap-btn');
            const result = document.getElementById('swap-result');
            btn.disabled = true; btn.innerHTML = 'Processing...'; result.style.display = 'none';
            try {
                const r = await fetch('/wbank/swap/apply', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({amount: amt})
                });
                const d = await r.json();
                if (d.success) {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">' +
                        'Swap successful!<br>' +
                        '<b>' + d.wtc_amount + ' WTC</b> → <b>HK$' + d.net_hkd + '</b><br>' +
                        '<span style="font-size:12px;">Rate: ' + d.rate + ' | Fee: HK$' + d.fee_hkd + '</span>' +
                        '</div>';
                    document.getElementById('swap-amount').value = '';
                    document.getElementById('swap-preview').style.display = 'none';
                    // Refresh balance
                    try { const b = await fetch('/wbank/web3/info'); const bd = await b.json();
                        if (bd.balance !== undefined && document.getElementById('main-balance'))
                            document.getElementById('main-balance').textContent = bd.balance; } catch(e) {}
                    loadSwapInfo();
                } else {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">' + (d.error || 'Swap failed') + '</div>';
                }
            } catch(e) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Error: ' + (e.message || '') + '</div>';
            }
            btn.disabled = false; btn.innerHTML = 'Apply Swap';
        }

        // Override showPage to load swap info
        const origShowPage = window.showPage || function(){};
        window.showPage = function(pageId) {
            origShowPage(pageId);
            if (pageId === 'swap') setTimeout(loadSwapInfo, 100);
        };
'''

if "function loadSwapInfo" not in client:
    client = client.replace('</script>', swap_client_js + '\n</script>')

open(CLIENT_TPL, "w", encoding="utf-8").write(client)
print("[OK] User panel UI updated")

print("\n=== Done! ===")
print("Restart server to apply changes")
