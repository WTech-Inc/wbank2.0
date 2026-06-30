"""Fix web3 frontend - better error handling for login state"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# Fix loadWeb3Info - show proper error when not logged in
old_web3 = '''        // === Web3 Wallet ===
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
        };'''

new_web3 = '''        // === Web3 Wallet ===
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
                // Update network info
                const netEl = document.querySelector('.web3-network');
                if (netEl) netEl.textContent = d.network || 'BSC Testnet';
            } catch(e) {
                console.log('Web3:', e);
                if (addrField) addrField.value = '載入失敗';
                if (histContainer) histContainer.innerHTML = '<p style="color:#ef4444;text-align:center;padding:20px;">⚠️ 網絡錯誤，請刷新頁面</p>';
            }
            // Load tx history
            try {
                const r2 = await fetch('/wbank/web3/history');
                const txns = await r2.json();
                if (!histContainer) return;
                if (txns.error) {
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
            } catch(e) {
                console.log('History:', e);
                if (histContainer) histContainer.innerHTML = '<p style="color:#ef4444;text-align:center;padding:20px;">⚠️ 載入失敗</p>';
            }
        }
        // Load web3 info on tab switch
        const origShowPage = showPage;
        showPage = function(pageId) {
            origShowPage(pageId);
            if (pageId === 'web3') setTimeout(loadWeb3Info, 100);
        };'''

if old_web3 in tpl:
    tpl = tpl.replace(old_web3, new_web3)
    open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8').write(tpl)
    print('[OK] Frontend web3 JS fixed - better error handling')
else:
    print('[WARN] Could not find old web3 JS')
    # Check what's there
    idx = tpl.find('// === Web3 Wallet ===')
    if idx >= 0:
        print(f'Current code at {idx}...')
    else:
        print('No Web3 Wallet section found')

print('\nDone')
