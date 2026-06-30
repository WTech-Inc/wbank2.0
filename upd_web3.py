with open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Send section after the warning box in the web3 section
old_warning = '''                <div style="background:#fff8e1;border:1px solid #ffe082;border-radius:8px;padding:12px;margin-bottom:16px;">
                    <p style="font-size:12px;color:#f57f17;margin:0;">
                        ⚠️ WTC (WCoins) 是基於 Ethereum ERC20 標準的數位代幣。
                        請確保只發送 WTC 到此地址，發送其他代幣可能導致資產損失。
                    </p>
                </div>'''

send_form = '''                <div style="background:#fff8e1;border:1px solid #ffe082;border-radius:8px;padding:12px;margin-bottom:16px;">
                    <p style="font-size:12px;color:#f57f17;margin:0;">
                        ⚠️ WTC (WCoins) 是基於 Ethereum ERC20 標準的數位代幣。
                        請確保只發送 WTC 到此地址，發送其他代幣可能導致資產損失。
                    </p>
                </div>

                <div style="background:white;border:1px solid #e8ecf1;border-radius:12px;padding:20px;margin-bottom:16px;">
                    <h4 style="margin:0 0 16px;font-size:16px;color:#1a1a2e;">📤 發送 WTC</h4>
                    <div style="margin-bottom:12px;">
                        <label style="font-size:13px;color:#64748b;display:block;margin-bottom:4px;">接收地址 (Ethereum 0x...)</label>
                        <input type="text" id="send-to" placeholder="0x..."
                               style="width:100%;padding:10px;border:1px solid #e2e8f0;border-radius:8px;font-size:14px;font-family:monospace;">
                    </div>
                    <div style="margin-bottom:16px;">
                        <label style="font-size:13px;color:#64748b;display:block;margin-bottom:4px;">數量 (WTC)</label>
                        <input type="number" id="send-amount" placeholder="0"
                               style="width:100%;padding:10px;border:1px solid #e2e8f0;border-radius:8px;font-size:14px;">
                    </div>
                    <button onclick="sendWTC()" id="send-btn"
                            style="width:100%;padding:12px;background:linear-gradient(135deg,#4fc3f7,#00bcd4);color:#0c0c1d;border:none;border-radius:8px;font-weight:600;font-size:15px;cursor:pointer;">
                        🔗 發送 WTC
                    </button>
                    <div id="send-result" style="margin-top:12px;display:none;"></div>
                </div>

                <div style="background:white;border:1px solid #e8ecf1;border-radius:12px;padding:20px;">
                    <h4 style="margin:0 0 12px;font-size:16px;color:#1a1a2e;">📜 交易記錄</h4>
                    <div id="tx-history" style="font-size:13px;color:#64748b;">載入中...</div>
                </div>'''

content = content.replace(old_warning, send_form)

# Add Web3 JavaScript for sending transactions
old_script = '''        // === Web3 Wallet ===
        function copyAddress() {'''

new_script = '''        // === Web3 Wallet ===
        async function loadWeb3Info() {
            try {
                const r = await fetch('/wbank/web3/info');
                const d = await r.json();
                if (d.address && document.getElementById('web3-address')) {
                    document.getElementById('web3-address').value = d.address;
                }
            } catch(e) { console.log('Web3:', e); }
            // Load tx history
            try {
                const r2 = await fetch('/wbank/web3/history');
                const txns = await r2.json();
                const container = document.getElementById('tx-history');
                if (!container) return;
                if (txns.length === 0) {
                    container.innerHTML = '<p style="color:#94a3b8;text-align:center;padding:20px;">暫無交易記錄</p>';
                } else {
                    container.innerHTML = txns.map(t =>
                        '<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">' +
                        '<span style="color:#1a1a2e;">' + t.action + '</span><br>' +
                        '<span style="color:#94a3b8;">' + t.time + '</span></div>'
                    ).join('');
                }
            } catch(e) { console.log('History:', e); }
        }
        // Load web3 info on tab switch
        const origShowPage = showPage;
        showPage = function(pageId) {
            origShowPage(pageId);
            if (pageId === 'web3') loadWeb3Info();
        };

        function copyAddress() {'''

content = content.replace(old_script, new_script)

# Add send function before copyAddress
old_copy = '''        function copyAddress() {'''
send_func = '''        async function sendWTC() {
            const to = document.getElementById('send-to').value.trim();
            const amount = document.getElementById('send-amount').value.trim();
            const btn = document.getElementById('send-btn');
            const result = document.getElementById('send-result');

            if (!to || !amount) { alert('請填寫接收地址和數量'); return; }
            if (!to.startsWith('0x') || to.length !== 42) { alert('請輸入有效的 Ethereum 地址 (0x...)'); return; }
            if (parseInt(amount) <= 0) { alert('數量必須大於 0'); return; }

            btn.disabled = true;
            btn.innerHTML = '⏳ 處理中...';
            result.style.display = 'none';

            try {
                const r = await fetch('/wbank/web3/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({to: to, amount: parseInt(amount)})
                });
                const d = await r.json();
                if (d.success) {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">'
                        + '✅ 成功發送 ' + d.amount + ' WTC<br>'
                        + 'TX: <a href="https://sepolia.etherscan.io/tx/' + d.tx_hash + '" target="_blank" style="color:#16a34a;font-size:12px;">'
                        + d.tx_hash.slice(0, 20) + '...' + d.tx_hash.slice(-8) + '</a>'
                        + '</div>';
                    // Refresh balance
                    const b = await fetch('/wbank/web3/info');
                    const bd = await b.json();
                    if (bd.balance !== undefined && document.getElementById('web3-balance')) {
                        document.getElementById('web3-balance').textContent = bd.balance;
                    }
                    loadWeb3Info();
                } else {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ ' + (d.error || '發送失敗') + '</div>';
                }
            } catch(e) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ 錯誤: ' + e.message + '</div>';
            }
            btn.disabled = false;
            btn.innerHTML = '🔗 發送 WTC';
        }

        function copyAddress() {'''
content = content.replace(old_copy, send_func)

with open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Web3 send form added to user panel')
