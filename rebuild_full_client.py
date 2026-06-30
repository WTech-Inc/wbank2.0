"""Rebuild wbankClient.html from scratch - clean version with MetaMask + Swap"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

WTC_CONTRACT = "0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB"
BASESCAN = "https://basescan.org"

tpl = '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WBank - {{ user.username }}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.js"></script>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:Segoe UI,sans-serif; background:#f5f7fa; }
        .top-bar { position:fixed; top:0; left:0; right:0; background:linear-gradient(135deg,#1a1a2e,#16213e); padding:16px 20px; display:flex; justify-content:space-between; align-items:center; z-index:100; color:white; }
        .top-bar .title { font-size:20px; font-weight:700; }
        .top-bar .user { font-size:13px; }
        .main-content { padding:80px 20px 80px; max-width:600px; margin:0 auto; }
        .page { display:none; }
        .page.active { display:block; }
        .card { background:white; border-radius:12px; padding:20px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06); }
        .card h3 { font-size:16px; margin-bottom:12px; color:#1a1a2e; }
        .balance-card { background:linear-gradient(135deg,#1a1a2e,#16213e); border-radius:12px; padding:24px; margin-bottom:16px; color:white; }
        .balance-card .balance { font-size:36px; font-weight:700; margin-top:8px; }
        .balance-card .balance span { color:#4fc3f7; }
        .balance-card .label { font-size:13px; color:rgba(255,255,255,0.5); }
        .nav-bar { position:fixed; bottom:0; left:0; right:0; background:white; display:flex; border-top:1px solid #e8ecf1; z-index:100; }
        .nav-item { flex:1; text-align:center; padding:12px 8px; cursor:pointer; font-size:11px; color:#94a3b8; }
        .nav-item:hover, .nav-item.active { color:#4fc3f7; }
        .btn { width:100%; padding:12px; border:none; border-radius:8px; font-weight:600; font-size:14px; cursor:pointer; }
        .btn-primary { background:linear-gradient(135deg,#4fc3f7,#00bcd4); color:#0c0c1d; }
        input { width:100%; padding:10px; border:1px solid #e2e8f0; border-radius:8px; font-size:13px; margin-bottom:8px; }
        .stat-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
        .stat-item { text-align:center; padding:16px; background:#f8fafc; border-radius:8px; }
        .stat-item .num { font-size:24px; font-weight:700; color:#1a1a2e; }
        .stat-item .lbl { font-size:11px; color:#94a3b8; }
    </style>
</head>
<body>
<div class="top-bar">
    <div class="title">WBank</div>
    <div class="user" style="display:flex;align-items:center;gap:12px;">
        <span>{{ user.username }}<span style="color:rgba(255,255,255,0.5);"> WBank</span></span>
        <a href="/wbank/auth/v1/logout" style="font-size:12px;color:#ef4444;text-decoration:none;padding:4px 10px;border:1px solid rgba(239,68,68,0.3);border-radius:6px;">Logout</a>
    </div>
</div>

<div class="main-content">
    <div id="home" class="page active">
        <div class="balance-card">
            <div class="label">Balance</div>
            <div class="balance">$<span id="main-balance">{{ balance }}</span></div>
            <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-top:4px;">HKD${{ "%.2f"|format(balance|int / 10) }}</div>
        </div>
        <div class="stat-grid">
            <div class="stat-item"><div class="num">${{ HK_Value }}</div><div class="lbl">HKD</div></div>
            <div class="stat-item"><div class="num">${{ tw_value }}</div><div class="lbl">TWD</div></div>
            <div class="stat-item"><div class="num">${{ US_value }}</div><div class="lbl">USD</div></div>
            <div class="stat-item"><div class="num" id="nav-balance">{{ balance }}</div><div class="lbl">WTC</div></div>
        </div>
        <div class="card">
            <h3>Account Info</h3>
            <p style="font-size:13px;color:#64748b;">Acc: {{ acc_number }}</p>
            <p style="font-size:13px;color:#64748b;">MFA: {{ "Enabled" if userMFA else "Disabled" }}</p>
        </div>
    </div>

    <div id="web3" class="page">
        <div class="card" style="text-align:center;">
            <div style="font-size:32px;">\U0001f517</div>
            <h2 style="color:#1a1a2e;">WTC Token</h2>
            <p style="font-size:13px;color:#94a3b8;">Base Mainnet</p>
        </div>
        <div class="balance-card">
            <div class="label">WTC Balance</div>
            <div class="balance"><span id="web3-balance">{{ balance }}</span></div>
            <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-top:4px;">
                Address: <span id="web3-address" style="cursor:pointer;" onclick="copyAddr()">{{ hash_card_number[:40] }}</span>
            </div>
        </div>
        <div class="card">
            <h3>Send WTC</h3>
            <input type="text" id="send-to" placeholder="Address 0x...">
            <input type="number" id="send-amount" placeholder="Amount">
            <button class="btn btn-primary" onclick="sendWTC()" id="send-btn">Send WTC</button>
            <div style="font-size:11px;color:#94a3b8;margin-top:4px;"> 50 WTC gas fee per tx</div>
            <div id="send-result" style="margin-top:12px;display:none;"></div>
        </div>
        <div class="card">
            <h3>Add to MetaMask</h3>
            <button onclick="addToMetaMask()" style="background:#f6851b;color:white;border:none;border-radius:8px;padding:10px 24px;font-weight:600;font-size:14px;cursor:pointer;"> Add to MetaMask</button>
            <div style="margin-top:12px;font-size:11px;color:#94a3b8;">
                Network: Base Mainnet (8453)<br>
                Contract: <span style="font-family:monospace;font-size:10px;">''' + WTC_CONTRACT + '''</span><br>
                <a href="''' + BASESCAN + '''/address/''' + WTC_CONTRACT + '''" target="_blank" style="color:#4fc3f7;">BaseScan</a>
            </div>
        </div>
        <div class="card">
            <h3>Transactions</h3>
            <div id="tx-history" style="font-size:13px;color:#94a3b8;">Loading...</div>
        </div>
        <div class="card" style="text-align:center;">
            <h3>QR Code</h3>
            <img src="data:image/svg+xml;base64,{{ img }}" width="200" height="200">
            <p style="font-size:11px;color:#94a3b8;">Scan to receive WTC</p>
        </div>
    </div>

    <div id="swap" class="page">
        <div class="card" style="text-align:center;">
            <div style="font-size:32px;">\U0001f4b1</div>
            <h2 style="color:#1a1a2e;">WTC/HKD Swap</h2>
            <p style="font-size:13px;color:#94a3b8;">Convert WTC to HKD digital cash</p>
        </div>
        <div class="balance-card" style="background:linear-gradient(135deg,#059669,#10b981);">
            <div class="label">Rate</div>
            <div class="balance" style="font-size:24px;"><span id="swap-rate-display">Loading...</span></div>
            <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:4px;">Fee: <span id="swap-fee-display">10%</span></div>
        </div>
        <div class="card">
            <h3>Swap WTC to HKD</h3>
            <input type="number" id="swap-amount" placeholder="WTC amount" oninput="updateSwapPreview()">
            <div id="swap-preview" style="display:none;background:#f0fdf4;padding:12px;border-radius:8px;margin-bottom:12px;">
                <div style="font-size:13px;color:#059669;">You will receive:</div>
                <div style="font-size:24px;font-weight:700;color:#059669;">HK$ <span id="swap-net"></span></div>
                <div style="font-size:12px;color:#64748b;margin-top:4px;">
                    Gross: HK$ <span id="swap-gross"></span> |
                    Fee (<span id="swap-fee-pct"></span>%): HK$ <span id="swap-fee"></span>
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
</div>

<div class="nav-bar">
    <div class="nav-item active" onclick="showPage('home')">\U0001f3e0<br>Home</div>
    <div class="nav-item" onclick="showPage('web3')">\U0001f517<br>Web3</div>
    <div class="nav-item" onclick="showPage('swap')">\U0001f4b1<br>Swap</div>
</div>

<script>
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(function(p) { p.classList.remove('active'); });
    var el = document.getElementById(pageId);
    if (el) el.classList.add('active');
    document.querySelectorAll('.nav-item').forEach(function(n) { n.classList.remove('active'); });
    document.querySelectorAll('[onclick*="' + pageId + '"]').forEach(function(n) { n.classList.add('active'); });
    if (pageId === 'web3') setTimeout(loadWeb3Info, 100);
    if (pageId === 'swap') setTimeout(loadSwapInfo, 100);
}

// === Web3 ===
async function loadWeb3Info() {
    var addrField = document.getElementById('web3-address');
    var histContainer = document.getElementById('tx-history');
    var balanceField = document.getElementById('web3-balance');
    try {
        var r = await fetch('/wbank/web3/info');
        var d = await r.json();
        if (d.error) {
            if (addrField) addrField.textContent = 'Login required';
            return;
        }
        if (d.address && addrField) addrField.textContent = d.address.slice(0,40);
        if (d.balance !== undefined && balanceField) balanceField.textContent = d.balance;
    } catch(e) { console.log('Web3 error:', e); }
    try {
        var r2 = await fetch('/wbank/web3/history');
        var txns = await r2.json();
        if (!histContainer) return;
        if (!txns || txns.length === 0) {
            histContainer.innerHTML = 'No transactions';
        } else {
            var html = '';
            for (var i = 0; i < txns.length; i++) {
                html += '<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">' +
                    '<span>' + (txns[i].action || '') + '</span><br>' +
                    '<span style="color:#94a3b8;">' + (txns[i].time || '') + '</span></div>';
            }
            histContainer.innerHTML = html;
        }
    } catch(e) { console.log('History error:', e); }
}

async function sendWTC() {
    var to = document.getElementById('send-to') ? document.getElementById('send-to').value.trim() : '';
    var amt = document.getElementById('send-amount') ? document.getElementById('send-amount').value.trim() : '';
    var btn = document.getElementById('send-btn');
    var result = document.getElementById('send-result');
    if (!to || !amt) { alert('Fill in address and amount'); return; }
    if (parseInt(amt) <= 0) { alert('Amount must be > 0'); return; }
    btn.disabled = true; btn.innerHTML = 'Processing...'; result.style.display = 'none';
    try {
        var r = await fetch('/wbank/web3/send', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({to: to, amount: parseInt(amt)})
        });
        var d = await r.json();
        if (d.success) {
            result.style.display = 'block';
            var explorerLink = d.tx_hash ? '<a href="https://basescan.org/tx/' + d.tx_hash + '" target="_blank" style="color:#16a34a;text-decoration:underline;">View on BaseScan</a>' : '';
            result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">Sent ' + d.amount + ' WTC (Fee: 50 WTC)<br>TX: ' + (d.tx_hash ? d.tx_hash.slice(0,20)+'...' : '') + '<br>' + explorerLink + '</div>';
            try { var b = await fetch('/wbank/web3/info'); var bd = await b.json(); if (bd.balance !== undefined && document.getElementById('web3-balance')) document.getElementById('web3-balance').textContent = bd.balance; } catch(e) {}
            loadWeb3Info();
        } else {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">' + (d.error || 'Failed') + '</div>';
        }
    } catch(e) {
        result.style.display = 'block';
        result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Error: ' + (e.message || '') + '</div>';
    }
    btn.disabled = false; btn.innerHTML = 'Send WTC';
}

async function addToMetaMask() {
    if (!window.ethereum) { alert('Install MetaMask!'); return; }
    try {
        await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [{ chainId: '0x2105', chainName: 'Base Mainnet', nativeCurrency: { name: 'ETH', symbol: 'ETH', decimals: 18 }, rpcUrls: ['https://mainnet.base.org'], blockExplorerUrls: ['https://basescan.org'] }]
        });
        var wasAdded = await window.ethereum.request({
            method: 'wallet_watchAsset',
            params: { type: 'ERC20', options: { address: "''' + WTC_CONTRACT + '''", symbol: 'WTC', decimals: 18 } }
        });
        if (wasAdded) alert('WTC added to MetaMask!');
    } catch(e) { alert(e.message || ''); }
}

function copyAddr() {
    var el = document.getElementById('web3-address');
    if (!el) return;
    var addr = '0x' + el.textContent;
    navigator.clipboard.writeText(addr).then(function() { alert('Address copied!'); }).catch(function() {
        var ta = document.createElement('textarea');
        ta.value = addr;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        alert('Address copied!');
    });
}

// === Swap ===
var swapRateData = {wtc: 10, hkd: 1, fee_percent: 10};

async function loadSwapInfo() {
    try {
        var r = await fetch('/wbank/swap/info');
        var d = await r.json();
        swapRateData = d;
        document.getElementById('swap-rate-display').textContent = d.rate_label;
        document.getElementById('swap-fee-display').textContent = d.fee_label;
        document.getElementById('swap-fee-pct').textContent = d.fee_percent;
    } catch(e) { document.getElementById('swap-rate-display').textContent = '10 WTC = 1 HKD'; }
    try {
        var r2 = await fetch('/wbank/web3/history');
        var txns = await r2.json();
        var container = document.getElementById('swap-history');
        if (!container) return;
        var swaps = [];
        for (var i = 0; i < txns.length; i++) {
            if (txns[i].action && txns[i].action.indexOf('SWAP') >= 0) swaps.push(txns[i]);
        }
        if (swaps.length === 0) {
            container.innerHTML = 'No swap history';
        } else {
            var html = '';
            for (var i = 0; i < swaps.length; i++) {
                html += '<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">' +
                    '<span>' + (swaps[i].action || '') + '</span><br>' +
                    '<span style="color:#94a3b8;">' + (swaps[i].time || '') + '</span></div>';
            }
            container.innerHTML = html;
        }
    } catch(e) { console.log('Swap history error:', e); }
}

function updateSwapPreview() {
    var amt = parseFloat(document.getElementById('swap-amount').value);
    var preview = document.getElementById('swap-preview');
    var btn = document.getElementById('swap-btn');
    if (!amt || amt <= 0) { preview.style.display = 'none'; btn.disabled = true; return; }
    var gross = amt * swapRateData.hkd / swapRateData.wtc;
    var fee = gross * swapRateData.fee_percent / 100;
    var net = gross - fee;
    document.getElementById('swap-gross').textContent = gross.toFixed(2);
    document.getElementById('swap-fee').textContent = fee.toFixed(2);
    document.getElementById('swap-net').textContent = net.toFixed(2);
    preview.style.display = 'block';
    btn.disabled = false;
}

async function applySwap() {
    var amt = parseInt(document.getElementById('swap-amount').value);
    if (!amt || amt <= 0) return;
    var btn = document.getElementById('swap-btn');
    var result = document.getElementById('swap-result');
    btn.disabled = true; btn.innerHTML = 'Processing...'; result.style.display = 'none';
    try {
        var r = await fetch('/wbank/swap/apply', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({amount: amt})
        });
        var text = await r.text();
        var d;
        try { d = JSON.parse(text); } catch(e) {
            result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Server error, try again</div>';
            result.style.display = 'block';
            btn.disabled = false; btn.innerHTML = 'Apply Swap';
            return;
        }
        if (d.success) {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">' +
                '<b>' + d.wtc_amount + ' WTC</b> to <b>HK$' + d.net_hkd + '</b><br>' +
                '<span style="font-size:12px;">Rate: ' + d.rate + ' | Fee: HK$' + d.fee_hkd + '</span></div>';
            document.getElementById('swap-amount').value = '';
            document.getElementById('swap-preview').style.display = 'none';
            try { var b = await fetch('/wbank/web3/info'); var bd = await b.json(); if (bd.balance && document.getElementById('main-balance')) document.getElementById('main-balance').textContent = bd.balance; } catch(e) {}
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
</script>
</body>
</html>'''

with open("E:/wbank/templates/wbankClient.html", "w", encoding="utf-8") as f:
    f.write(tpl)

print(f"OK - Rebuilt wbankClient.html ({len(tpl)} bytes)")
