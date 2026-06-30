"""Fix user panel - separate SocketIO script from Web3 JS"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# Fix 1: Split the SocketIO + Web3 JS into separate script tags
old = '''    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.js">

        // === Web3 Wallet Functions ===
        async function loadWeb3Info() {
            const addrField = document.getElementById('web3-address');
            const histContainer = document.getElementById('tx-history');
            const balanceField = document.getElementById('web3-balance');
            try {
                const r = await fetch('/wbank/web3/info');
                const d = await r.json();
                if (d.error) {
                    if (addrField) addrField.value = '請先登入';
                    if (histContainer) histContainer.innerHTML = '<p style="color:#ef4444;text-align:center;padding:20px;">⚠️ ' + d.error + '</p>';
                    return;
                }
                if (d.address && addrField) addrField.value = d.address;
                if (d.balance !== undefined && balanceField) balanceField.textContent = d.balance;
            } catch(e) { console.log('Web3:', e); }
            try {
                const r2 = await fetch('/wbank/web3/history');
                const txns = await r2.json();
                if (!histContainer) return;
                if (txns && txns.error) {
                    histContainer.innerHTML = '<p style="color:#ef4444;text-align:center;padding:20px;">⚠️ ' + txns.error + '</p>';
                    return;
                }
                if (!txns || txns.length === 0) {
                    histContainer.innerHTML = '<p style="color:#94a3b8;text-align:center;padding:20px;">暫無交易記錄</p>';
                } else {
                    histContainer.innerHTML = txns.map(t =>
                        '<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">' +
                        '<span style="color:#1a1a2e;">' + (t.action || '') + '</span><br>' +
                        '<span style="color:#94a3b8;">' + (t.time || '') + '</span></div>'
                    ).join('');
                }
            } catch(e) { console.log('History:', e); }
        }

        async function sendWTC() {
            const to = document.getElementById('send-to').value.trim();
            const amount = document.getElementById('send-amount').value.trim();
            const btn = document.getElementById('send-btn');
            const result = document.getElementById('send-result');
            if (!to || !amount) { alert('請填寫接收地址和數量'); return; }
            if (!to.startsWith('0x') || to.length !== 42) { alert('請輸入有效的 Ethereum 地址 (0x...)'); return; }
            if (parseInt(amount) <= 0) { alert('數量必須大於 0'); return; }
            btn.disabled = true; btn.innerHTML = '⏳ 處理中...'; result.style.display = 'none';
            try {
                const r = await fetch('/wbank/web3/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({to: to, amount: parseInt(amount)})
                });
                const d = await r.json();
                if (d.success) {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">' + '✅ 成功發送 ' + d.amount + ' WTC<br>TX: ' + (d.tx_hash ? d.tx_hash.slice(0, 20) + '...' : '') + '</div>';
                    try { const b = await fetch('/wbank/web3/info'); const bd = await b.json(); if (bd.balance !== undefined && document.getElementById('web3-balance')) document.getElementById('web3-balance').textContent = bd.balance; } catch(e) {}
                    loadWeb3Info();
                } else {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ ' + (d.error || '發送失敗') + '</div>';
                }
            } catch(e) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ 錯誤: ' + (e.message || '網絡錯誤') + '</div>';
            }
            btn.disabled = false; btn.innerHTML = '🔗 發送 WTC';
        }

        function copyAddress() {
            const addr = document.getElementById('web3-address');
            if (addr) { addr.select(); document.execCommand('copy'); alert('地址已複製'); }
        }

        // Load web3 info on tab switch

        };
        // === END Web3 Wallet ==='''

new = '''    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.js"></script>
    <script>
        // === Web3 Wallet Functions ===
        async function loadWeb3Info() {
            const addrField = document.getElementById('web3-address');
            const histContainer = document.getElementById('tx-history');
            const balanceField = document.getElementById('web3-balance');
            try {
                const r = await fetch('/wbank/web3/info');
                const d = await r.json();
                if (d.error) {
                    if (addrField) addrField.value = '請先登入';
                    if (histContainer) histContainer.innerHTML = '<p style="color:#ef4444;text-align:center;padding:20px;">\\u26a0\\ufe0f ' + d.error + '</p>';
                    return;
                }
                if (d.address && addrField) addrField.value = d.address;
                if (d.balance !== undefined && balanceField) balanceField.textContent = d.balance;
            } catch(e) { console.log('Web3:', e); }
            try {
                const r2 = await fetch('/wbank/web3/history');
                const txns = await r2.json();
                if (!histContainer) return;
                if (txns && txns.error) {
                    histContainer.innerHTML = '<p style="color:#ef4444;text-align:center;padding:20px;">\\u26a0\\ufe0f ' + txns.error + '</p>';
                    return;
                }
                if (!txns || txns.length === 0) {
                    histContainer.innerHTML = '<p style="color:#94a3b8;text-align:center;padding:20px;">暫無交易記錄</p>';
                } else {
                    histContainer.innerHTML = txns.map(t =>
                        '<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">' +
                        '<span style="color:#1a1a2e;">' + (t.action || '') + '</span><br>' +
                        '<span style="color:#94a3b8;">' + (t.time || '') + '</span></div>'
                    ).join('');
                }
            } catch(e) { console.log('History:', e); }
        }

        async function sendWTC() {
            const to = document.getElementById('send-to').value.trim();
            const amt = document.getElementById('send-amount').value.trim();
            const btn = document.getElementById('send-btn');
            const result = document.getElementById('send-result');
            if (!to || !amt) { alert('請填寫接收地址和數量'); return; }
            if (!to.startsWith('0x') || to.length !== 42) { alert('請輸入有效的地址'); return; }
            if (parseInt(amt) <= 0) { alert('數量必須大於 0'); return; }
            btn.disabled = true; btn.innerHTML = '⏳ 處理中...'; result.style.display = 'none';
            try {
                const r = await fetch('/wbank/web3/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({to: to, amount: parseInt(amt)})
                });
                const d = await r.json();
                if (d.success) {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">\\u2705 成功發送 ' + d.amount + ' WTC<br>TX: ' + (d.tx_hash ? d.tx_hash.slice(0,20)+'...' : '') + '</div>';
                    try { const b = await fetch('/wbank/web3/info'); const bd = await b.json(); if (bd.balance && document.getElementById('web3-balance')) document.getElementById('web3-balance').textContent = bd.balance; } catch(e) {}
                    loadWeb3Info();
                } else {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">\\u274c ' + (d.error || '發送失敗') + '</div>';
                }
            } catch(e) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">\\u274c ' + (e.message || '網絡錯誤') + '</div>';
            }
            btn.disabled = false; btn.innerHTML = '🔗 發送 WTC';
        }

        function copyAddress() {
            const a = document.getElementById('web3-address');
            if (a) { a.select(); document.execCommand('copy'); }
        }
        // === END Web3 Wallet ===
    </script>'''

if old in tpl:
    tpl = tpl.replace(old, new)
    print('[OK] Fixed SocketIO + Web3 script separation')
else:
    print('[WARN] Pattern not found, trying different approach...')
    # Try to find and fix the broken script tag
    idx = tpl.find('<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/')
    if idx >= 0:
        close = tpl.find('</script>', idx)
        if close > 0:
            # Extract content between the tags
            content = tpl[idx:close + 9]
            new_content = content.replace('></script>', '></script>\n    <script>\n') + '\n    </script>'
            tpl = tpl.replace(content, new_content)
            print(f'[OK] Split script tag at position {idx}')

# Also remove ALL old showPage overrides and duplicate loadWeb3Info
tpl = re.sub(
    r'const origShowPage = showPage;.*?if \(pageId === \'web3\'\) setTimeout\(loadWeb3Info, 100\);',
    '',
    tpl,
    flags=re.DOTALL
)

# Remove the final override from earlier fix that didn't work
tpl = re.sub(
    r'<script>\n// === CLEAN Web3 Wallet \(final\) ===.*?</script>',
    '',
    tpl,
    flags=re.DOTALL
)

# Remove any extra script tags that have stray code
tpl = re.sub(
    r'<script>\s*\n\s*\}\s*;\s*\n\s*// === END Web3 Wallet ===\s*\n\s*</script>',
    '',
    tpl,
    flags=re.DOTALL
)

open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8').write(tpl)

# Count remaining issues
print(f'loadWeb3Info count: {tpl.count("async function loadWeb3Info")}')
print(f'sendWTC count: {tpl.count("async function sendWTC")}')
print(f'script src socket.io: {"<script src" in tpl and "socket.io" in tpl}')

print('\nRestart server')
