"""Rebuild wbankClient.html template from scratch with working JS"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>泓財WBank - {{ user.username }} 頁面</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.js"></script>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Segoe UI',sans-serif; background:#f5f7fa; min-height:100vh; }
        .top-bar { position:fixed; top:0; left:0; right:0; background:linear-gradient(135deg,#1a1a2e,#16213e); padding:16px 20px; display:flex; justify-content:space-between; align-items:center; z-index:100; color:white; }
        .top-bar .title { font-size:20px; font-weight:700; background:linear-gradient(135deg,#4fc3f7,#00bcd4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
        .top-bar .user { font-size:13px; color:rgba(255,255,255,0.5); }
        .top-bar .user span { color:#4fc3f7; }
        .main-content { padding:80px 20px 80px; max-width:600px; margin:0 auto; }

        .page { display:none; }
        .page.active { display:block; }

        .card { background:white; border-radius:12px; padding:20px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06); }
        .card h3 { font-size:16px; margin-bottom:12px; color:#1a1a2e; }

        .balance-card { background:linear-gradient(135deg,#1a1a2e,#16213e); border-radius:12px; padding:24px; margin-bottom:16px; color:white; }
        .balance-card .balance { font-size:36px; font-weight:700; margin-top:8px; }
        .balance-card .balance span { background:linear-gradient(135deg,#4fc3f7,#00bcd4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
        .balance-card .label { font-size:13px; color:rgba(255,255,255,0.5); }

        .nav-bar { position:fixed; bottom:0; left:0; right:0; background:white; display:flex; border-top:1px solid #e8ecf1; z-index:100; padding-bottom:env(safe-area-inset-bottom); }
        .nav-item { flex:1; text-align:center; padding:12px 8px; cursor:pointer; font-size:11px; color:#94a3b8; transition:color 0.2s; }
        .nav-item i { display:block; font-size:20px; margin-bottom:4px; }
        .nav-item:hover { color:#4fc3f7; }
        .nav-item.active { color:#4fc3f7; }

        .btn { width:100%; padding:12px; border:none; border-radius:8px; font-weight:600; font-size:14px; cursor:pointer; transition:transform 0.2s; }
        .btn-primary { background:linear-gradient(135deg,#4fc3f7,#00bcd4); color:#0c0c1d; }
        .btn-primary:hover { transform:translateY(-1px); }
        .btn-secondary { background:#f1f5f9; color:#64748b; }

        input, textarea, select { width:100%; padding:10px; border:1px solid #e2e8f0; border-radius:8px; font-size:13px; margin-bottom:8px; }
        input:focus { border-color:#4fc3f7; outline:none; }

        .stat-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
        .stat-item { text-align:center; padding:16px; background:#f8fafc; border-radius:8px; }
        .stat-item .num { font-size:24px; font-weight:700; color:#1a1a2e; }
        .stat-item .lbl { font-size:11px; color:#94a3b8; margin-top:4px; }
    </style>
</head>
<body>
    <div class="top-bar">
        <div class="title">WBank</div>
        <div class="user">{{ user.username }}<span> · 泓財銀行</span></div>
    </div>

    <div class="main-content">
        <div id="home" class="page active">
            <div class="balance-card">
                <div class="label">帳戶餘額</div>
                <div class="balance">$<span id="main-balance">{{ balance }}</span></div>
                <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-top:4px;">≈ HKD${{ "%.2f"|format(balance|int / 10) }}</div>
            </div>
            <div class="stat-grid">
                <div class="stat-item"><div class="num">${{ HK_Value }}</div><div class="lbl">HKD</div></div>
                <div class="stat-item"><div class="num">${{ tw_value }}</div><div class="lbl">TWD</div></div>
                <div class="stat-item"><div class="num">${{ US_value }}</div><div class="lbl">USD</div></div>
                <div class="stat-item"><div class="num" id="nav-balance">{{ balance }}</div><div class="lbl">WTC</div></div>
            </div>
            <div class="card">
                <h3>賬戶資訊</h3>
                <p style="font-size:13px;color:#64748b;">賬號: {{ acc_number }}</p>
                <p style="font-size:13px;color:#64748b;">MFA: {{ "已啟用" if userMFA else "未啟用" }}</p>
            </div>
        </div>

        <div id="web3" class="page">
            <div class="card">
                <div style="font-size:32px;margin-bottom:8px;">🔗</div>
                <h2 style="color:#1a1a2e;">WTC Token</h2>
                <p style="font-size:13px;color:#94a3b8;">Base Mainnet</p>
            </div>

            <div class="balance-card">
                <div class="label">WTC 餘額</div>
                <div class="balance"><span id="web3-balance">{{ balance }}</span></div>
                <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-top:4px;">Address: 0x<span id="web3-address">{{ hash_card_number[:40] }}</span></div>
            </div>

            <div class="card">
                <h3>📤 發送 WTC</h3>
                <input type="text" id="send-to" placeholder="接收地址 0x...">
                <input type="number" id="send-amount" placeholder="數量">
                <button class="btn btn-primary" onclick="sendWTC()" id="send-btn">🔗 發送 WTC</button>
                <div id="send-result" style="margin-top:12px;display:none;"></div>
            </div>

            <div class="card">
                <h3>📜 交易紀錄</h3>
                <div id="tx-history" style="font-size:13px;color:#94a3b8;">載入中...</div>
            </div>

            <div class="card">
                <h3>📷 收款 QR</h3>
                <div style="text-align:center;">
                    <img src="data:image/svg+xml;base64,{{ img }}" width="200" height="200">
                    <p style="font-size:11px;color:#94a3b8;margin-top:8px;">掃碼接收 WTC</p>
                </div>
            </div>
        </div>

        <div id="swap" class="page">
            <div class="card" style="text-align:center;">
                <div style="font-size:32px;margin-bottom:8px;">💱</div>
                <h2 style="color:#1a1a2e;">WTC/HKD Swap</h2>
            </div>

            <div class="balance-card">
                <div class="label">Current Rate</div>
                <div class="balance" style="font-size:24px;"><span id="swap-rate">Loading...</span></div>
                <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:4px;">Fee: <span id="swap-fee">10%</span></div>
            </div>

            <div class="card">
                <h3>Swap WTC to HKD</h3>
                <input type="number" id="swap-amount" placeholder="WTC amount" oninput="previewSwap()">
                <div id="swap-preview" style="display:none;background:#f0fdf4;padding:12px;border-radius:8px;margin-bottom:12px;">
                    <div style="font-size:13px;color:#64748b;">You will receive:</div>
                    <div style="font-size:24px;font-weight:700;color:#059669;">HK$ <span id="swap-net"></span></div>
                    <div style="font-size:12px;color:#64748b;margin-top:4px;">Fee: HK$ <span id="swap-fee-amt"></span></div>
                </div>
                <button class="btn btn-primary" onclick="applySwap()" id="swap-btn" disabled>Apply Swap</button>
                <div id="swap-result" style="margin-top:12px;display:none;"></div>
            </div>

            <div class="card">
                <h3>Swap History</h3>
                <div id="swap-history" style="font-size:13px;color:#94a3b8;">Loading...</div>
            </div>
        </div>
    </div>

    <div class="nav-bar">
        <div class="nav-item active" onclick="showPage('home')">🏠<br>主頁</div>
        <div class="nav-item" onclick="showPage('web3')">🔗<br>Web3</div>
        <div class="nav-item" onclick="showPage('swap')">💱<br>Swap</div>
    </div>

    <script>
    // ===== Page Navigation =====
    function showPage(pageId) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        const el = document.getElementById(pageId);
        if (el) el.classList.add('active');
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.querySelectorAll(`[onclick="showPage('${pageId}')"]`).forEach(n => n.classList.add('active'));
        if (pageId === 'web3') setTimeout(loadWeb3Info, 100);
        if (pageId === 'swap') setTimeout(loadSwapInfo, 100);
    }

    // ===== Web3 =====
    async function loadWeb3Info() {
        const addrField = document.getElementById('web3-address');
        const histContainer = document.getElementById('tx-history');
        const balanceField = document.getElementById('web3-balance');
        try {
            const r = await fetch('/wbank/web3/info');
            const d = await r.json();
            if (d.error) {
                if (addrField) addrField.textContent = '請先登入';
                if (histContainer) histContainer.innerHTML = '<p style="color:#ef4444;">⚠️ ' + d.error + '</p>';
                return;
            }
            if (d.address && addrField) addrField.textContent = d.address.slice(0,40);
            if (d.balance !== undefined && balanceField) balanceField.textContent = d.balance;
        } catch(e) { console.log('Web3:', e); }
        try {
            const r2 = await fetch('/wbank/web3/history');
            const txns = await r2.json();
            if (!histContainer) return;
            if (txns && txns.error) {
                histContainer.innerHTML = '<p style="color:#ef4444;">⚠️ ' + txns.error + '</p>';
                return;
            }
            if (!txns || txns.length === 0) {
                histContainer.innerHTML = '<p style="color:#94a3b8;">暫無交易記錄</p>';
            } else {
                histContainer.innerHTML = txns.map(t =>
                    '<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">' +
                    '<span>' + (t.action || '') + '</span><br>' +
                    '<span style="color:#94a3b8;">' + (t.time || '') + '</span></div>'
                ).join('');
            }
        } catch(e) { console.log('History:', e); }
    }

    async function sendWTC() {
        const to = document.getElementById('send-to')?.value.trim();
        const amt = document.getElementById('send-amount')?.value.trim();
        const btn = document.getElementById('send-btn');
        const result = document.getElementById('send-result');
        if (!to || !amt) { alert('請填寫接收地址和數量'); return; }
        if (!to.startsWith('0x') || to.length !== 42) { alert('請輸入有效的地址'); return; }
        if (parseInt(amt) <= 0) { alert('數量必須大於 0'); return; }
        btn.disabled = true; btn.innerHTML = '處理中...'; result.style.display = 'none';
        try {
            const r = await fetch('/wbank/web3/send', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({to, amount: parseInt(amt)}) });
            const d = await r.json();
            if (d.success) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">✅ 成功發送 ' + d.amount + ' WTC<br>TX: ' + (d.tx_hash ? d.tx_hash.slice(0,20)+'...' : '') + '</div>';
                try { const b = await fetch('/wbank/web3/info'); const bd = await b.json(); if (bd.balance !== undefined && document.getElementById('web3-balance')) document.getElementById('web3-balance').textContent = bd.balance; } catch(e) {}
                loadWeb3Info();
            } else {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ ' + (d.error || '發送失敗') + '</div>';
            }
        } catch(e) {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ ' + (e.message || '網路錯誤') + '</div>';
        }
        btn.disabled = false; btn.innerHTML = '🔗 發送 WTC';
    }

    // ===== Swap =====
    var swapRate = {wtc:10, hkd:1, fee:10};

    function loadSwapInfo() {
        fetch('/wbank/swap/info').then(r => r.json()).then(d => {
            swapRate = d;
            document.getElementById('swap-rate').textContent = d.rate_label;
            document.getElementById('swap-fee').textContent = d.fee_label;
        }).catch(function(){});
        fetch('/wbank/swap/history').then(r => r.json()).then(list => {
            var el = document.getElementById('swap-history');
            if (!el) return;
            if (!list || list.length === 0) { el.innerHTML = 'No swap history'; return; }
            var h = '';
            for (var i = 0; i < list.length; i++) {
                var r = list[i];
                h += '<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;display:flex;justify-content:space-between;">';
                h += '<div><b>' + r.wtc_amount + ' WTC</b> → HK$' + r.amount + '</div>';
                h += '<div>' + r.status + '</div></div>';
            }
            el.innerHTML = h;
        }).catch(function(){});
    }

    function previewSwap() {
        var amt = document.getElementById('swap-amount').value;
        var preview = document.getElementById('swap-preview');
        var btn = document.getElementById('swap-btn');
        if (!amt || parseFloat(amt) <= 0) { preview.style.display = 'none'; btn.disabled = true; return; }
        var gross = amt * swapRate.hkd / swapRate.wtc;
        var fee = gross * (swapRate.fee_percent || 10) / 100;
        var net = gross - fee;
        document.getElementById('swap-net').textContent = net.toFixed(2);
        document.getElementById('swap-fee-amt').textContent = fee.toFixed(2);
        preview.style.display = 'block';
        btn.disabled = false;
    }

    function applySwap() {
        var amt = parseInt(document.getElementById('swap-amount').value);
        if (!amt || amt <= 0) return;
        var btn = document.getElementById('swap-btn');
        var result = document.getElementById('swap-result');
        btn.disabled = true; btn.textContent = 'Processing...'; result.style.display = 'none';
        fetch('/wbank/swap/apply', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({amount: amt})
        }).then(r => r.json()).then(d => {
            if (d.success) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">✅ Swapped ' + d.wtc_amount + ' WTC → HK$' + d.net_hkd + '<br>Fee: HK$' + d.fee_hkd + '</div>';
                document.getElementById('swap-amount').value = '';
                document.getElementById('swap-preview').style.display = 'none';
                loadSwapInfo();
            } else {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ ' + (d.error || 'Failed') + '</div>';
            }
            btn.disabled = false; btn.textContent = 'Apply Swap';
        }).catch(function(e) {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Error</div>';
            btn.disabled = false; btn.textContent = 'Apply Swap';
        });
    }

    // Auto load web3 on page load
    if (window.location.hash === '#web3') setTimeout(loadWeb3Info, 200);
    if (window.location.hash === '#swap') setTimeout(loadSwapInfo, 200);
    </script>
</body>
</html>'''

with open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8') as f:
    f.write(tpl)

print(f'[OK] Rebuilt wbankClient.html ({len(tpl)} bytes)')
print('[OK] Restart server')
