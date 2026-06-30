import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# Fix sendWTC - better error handling
old_send = '''        async function sendWTC() {
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
        }'''

new_send = '''        async function sendWTC() {
            const to = document.getElementById('send-to').value.trim();
            const amount = document.getElementById('send-amount').value.trim();
            const btn = document.getElementById('send-btn');
            const result = document.getElementById('send-result');

            if (!to || !amount) { alert('請填寫接收地址和數量'); return; }
            if (!to.startsWith('0x') || to.length !== 42) { alert('請輸入有效的 Ethereum 地址 (0x...)'); return; }
            if (parseInt(amount) <= 0) { alert('數量必須大於 0'); return; }
            if (parseInt(amount) > parseInt(document.getElementById('web3-balance').textContent || '0')) {
                alert('餘額不足'); return;
            }

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
                        + 'TX: ' + (d.tx_hash ? d.tx_hash.slice(0, 20) + '...' : '') + ''
                        + (d.tx_success ? ' <span style="color:#16a34a;font-size:11px;">✓ On-chain</span>' : ' <span style="color:#f59e0b;font-size:11px;">⚡ Off-chain</span>')
                        + '</div>';
                    // Refresh balance
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
                    result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ ' + (d.error || '發送失敗') + '</div>';
                }
            } catch(e) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ 錯誤: ' + (e.message || '網絡錯誤') + '</div>';
            }
            btn.disabled = false;
            btn.innerHTML = '🔗 發送 WTC';
        }'''

if old_send in tpl:
    tpl = tpl.replace(old_send, new_send)
    open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8').write(tpl)
    print('[OK] sendWTC function fixed')
else:
    print('[WARN] Could not find old sendWTC')
    idx = tpl.find('async function sendWTC')
    if idx >= 0:
        print(f'Found at {idx}')
        print(tpl[idx:idx+1000])

print('Done')
