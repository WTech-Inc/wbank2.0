    function showPage(pageId) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        const el = document.getElementById(pageId);
        if (el) el.classList.add('active');
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.querySelectorAll(`[onclick="showPage('${pageId}')"]`).forEach(n => n.classList.add('active'));
        if (pageId === 'web3') setTimeout(loadWeb3Info, 100);
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

    // Auto load web3 on page load
    if (window.location.hash === '#web3') setTimeout(loadWeb3Info, 200);
    
        async function addToMetaMask() {
            if (!window.ethereum) {
                alert('');
                return;
            }
            try {
                await window.ethereum.request({
                    method: 'wallet_addEthereumChain',
                    params: [{
                        chainId: '0x2105',
                        chainName: 'Base Mainnet',
                        nativeCurrency: { name: 'ETH', symbol: 'ETH', decimals: 18 },
                        rpcUrls: ['https://mainnet.base.org'],
                        blockExplorerUrls: ['https://basescan.org']
                    }]
                });
                const wasAdded = await window.ethereum.request({
                    method: 'wallet_watchAsset',
                    params: {
                        type: 'ERC20',
                        options: {
                            address: "0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB",
                            symbol: 'WTC',
                            decimals: 18
                        }
                    }
                });
                if (wasAdded) alert('WTC MetaMask!');
            } catch(e) {
                alert(e.message || '');
            }
        }
        function copyAddr() {
            const el = document.getElementById('web3-address');
            if (!el) return;
            const addr = '0x' + el.textContent;
            navigator.clipboard.writeText(addr).then(function() {
                alert('');
            }).catch(function() {
                var ta = document.createElement('textarea');
                ta.value = addr;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
                alert('');
            });
        }

    
        // === WTC/HKD Swap ===
        let swapRate = {wtc: 10, hkd: 1, fee: 10};

        async function loadSwapInfo() {
            try {
                const r = await fetch('/wbank/swap/info');
                const d = await r.json();
                swapRate = d;
                document.getElementById('swap-rate-display').textContent = d.rate_label;
                document.getElementById('swap-fee-display').textContent = d.fee_label;
                document.getElementById('swap-fee-pct').textContent = swapRate.fee_percent;
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
            const fee = gross * swapRate.fee_percent / 100;
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
result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Error: ' + (e.message || '') + '</div>'; + (d.error || 'Swap failed') + '</div>';
            }
            btn.disabled = false; btn.innerHTML = 'Apply Swap';
        }

        // Override showPage to load swap info
        const origShowPage = window.showPage || function(){};
        window.showPage = function(pageId) {
            origShowPage(pageId);
            if (pageId === 'swap') setTimeout(loadSwapInfo, 100);
        };

