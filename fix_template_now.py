"""Fix template by appending clean override at end"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# Add clean JS right before </body> that fixes everything
clean_js = '''
<script>
// === FINAL Web3 Wallet OVERRIDE ===
// (Overwrites all broken duplicates above)
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
    const to = document.getElementById('send-to')?.value.trim();
    const amt = document.getElementById('send-amount')?.value.trim();
    const btn = document.getElementById('send-btn');
    const result = document.getElementById('send-result');
    if (!to || !amt) { alert('請填寫接收地址和數量'); return; }
    if (!to.startsWith('0x') || to.length !== 42) { alert('請輸入有效的地址'); return; }
    if (parseInt(amt) <= 0) { alert('數量必須大於 0'); return; }
    btn.disabled = true; btn.innerHTML = '&#x23f3; 處理中...'; result.style.display = 'none';
    try {
        const r = await fetch('/wbank/web3/send', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({to, amount: parseInt(amt)})
        });
        const d = await r.json();
        if (d.success) {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">&#x2705; 成功發送 ' + d.amount + ' WTC<br>TX: ' + (d.tx_hash ? d.tx_hash.slice(0,20)+'...' : '') + '</div>';
            try {
                const b = await fetch('/wbank/web3/info');
                const bd = await b.json();
                if (bd.balance !== undefined && document.getElementById('web3-balance')) {
                    document.getElementById('web3-balance').textContent = bd.balance;
                }
            } catch(e) {}
            loadWeb3Info();
        } else {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">&#x274c; ' + (d.error || '發送失敗') + '</div>';
        }
    } catch(e) {
        result.style.display = 'block';
        result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">&#x274c; ' + (e.message || '網絡錯誤') + '</div>';
    }
    btn.disabled = false; btn.innerHTML = '&#x1f517; 發送 WTC';
}

// Fix showPage to also trigger loadWeb3Info
(function() {
    if (typeof showPage === 'function') {
        const _orig = showPage;
        showPage = function(id) {
            _orig(id);
            if (id === 'web3') setTimeout(loadWeb3Info, 200);
        };
    }
})();
</script>
'''

if '</body>' in tpl:
    tpl = tpl.replace('</body>', clean_js + '\n</body>')
    open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8').write(tpl)
    print(f'[OK] Clean JS override added ({len(clean_js)} chars)')
    print('[OK] Restart server')
else:
    print('[ERR] No </body> found')
