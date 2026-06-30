
function showPage(id, el) {
    document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active')});
    var page = document.getElementById(id);
    if (page) page.classList.add('active');
    document.querySelectorAll('.nav-item').forEach(function(n){n.classList.remove('active')});
    if (el) el.classList.add('active');
    if (id === 'web3') setTimeout(loadWCoinsInfo, 100);
    if (id === 'swap') setTimeout(loadSwapInfo, 100);
        if (id === 'withdraw') setTimeout(loadWithdrawInfo, 100);
        if (id === 'settings') setTimeout(loadSettingsInfo, 100);
}

function copyText(id) {
    var el = document.getElementById(id);
    if (!el) return;
    var t = el.textContent;
    navigator.clipboard.writeText(t).then(function(){alert('Copied!')}).catch(function(){
        var ta = document.createElement('textarea');
        ta.value = t; document.body.appendChild(ta); ta.select();
        document.execCommand('copy'); document.body.removeChild(ta);
        alert('Copied!');
    });
}

function loadWCoinsInfo() {
    var x = new XMLHttpRequest();
    x.onreadystatechange = function() {
        if (x.readyState == 4 && x.status == 200) {
            try {
                var d = JSON.parse(x.responseText);
                if (d && d.address) {
                    document.getElementById('wcoins-balance').textContent = d.balance;
                    document.getElementById('wcoins-address').textContent = d.address;
                }
            } catch(e) {}
        }
    };
    x.open('GET', '/wcoins/api/address', true);
    x.send();

    var x2 = new XMLHttpRequest();
    x2.onreadystatechange = function() {
        if (x2.readyState == 4 && x2.status == 200) {
            try {
                var de = JSON.parse(x2.responseText);
                if (de && de.eth_address) {
                    document.getElementById('wcoins-eth-address').textContent = de.eth_address;
                    document.getElementById('wcoins-receive-eth').textContent = de.eth_address;
                }
            } catch(e) {}
        }
    };
    x2.open('GET', '/wcoins/api/eth_address', true);
    x2.send();
    
    // Calculate HKD/USD value (based on 10 WCN ≈ 1 HKD ≈ 0.128 USD)
    var balEl = document.getElementById('wcoins-balance');
    if (balEl) {
        var bal = parseFloat(balEl.textContent) || 0;
        var hkd = (bal / 10).toFixed(2);
        var usd = (bal / 10 * 0.128).toFixed(2);
        var hkdEl = document.getElementById('wcoins-hkd-value');
        var usdEl = document.getElementById('wcoins-usd-value');
        if (hkdEl) hkdEl.textContent = hkd;
        if (usdEl) usdEl.textContent = usd;
    }

    var x3 = new XMLHttpRequest();
    x3.onreadystatechange = function() {
        if (x3.readyState == 4 && x3.status == 200) {
            try {
                var txns = JSON.parse(x3.responseText);
                var el = document.getElementById('wcoins-tx-history');
                if (!el) return;
                var list = txns && txns.transactions || [];
                if (list.length === 0) { el.innerHTML = '<div style="text-align:center;padding:30px 0;"><div style="font-size:40px;margin-bottom:10px;">📭</div><div style="color:#94a3b8;font-size:13px;">No transactions yet</div></div>'; return; }
                var h = '';
                for (var i = 0; i < list.length; i++) {
                    var tx = list[i];
                    var isSent = tx.type === 'sent';
                    var icon = isSent ? '\u2197' : '\u2199';
                    var color = isSent ? '#ef4444' : '#22c55e';
                    var bgColor = isSent ? '#fef2f2' : '#f0fdf4';
                    var other = isSent ? tx.receiver : tx.sender;
                    var otherLabel = isSent ? 'To' : 'From';
                    var shortOther = other && other.length > 15 ? other.slice(0,6)+'...'+other.slice(-4) : (other || '?');
                    var time = tx.created_at || '';
                    if (time.length > 10) time = time.slice(0, 16);
                    h += '<div style="padding:10px;margin-bottom:8px;border-radius:10px;font-size:13px;display:flex;justify-content:space-between;align-items:center;background:'+bgColor+';">';
                    h += '<div style="display:flex;align-items:center;gap:10px;">';
                    h += '<div style="width:36px;height:36px;min-width:36px;border-radius:50%;background:'+color+';color:white;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:bold;">'+icon+'</div>';
                    h += '<div><div style="font-weight:600;color:#1e293b;font-size:14px;">'+tx.amount+' WCN</div>';
                    h += '<div style="color:#64748b;font-size:11px;">'+otherLabel+': '+shortOther+'</div></div></div>';
                    h += '<div style="text-align:right;"><div style="font-size:11px;font-weight:500;color:'+color+';">#'+tx.block_index+'</div>';
                    h += '<div style="color:#94a3b8;font-size:10px;">'+time+'</div></div></div>';
                }
                el.innerHTML = h;
            } catch(e) {}
        }
    };
    x3.open('GET', '/wcoins/api/history', true);
    x3.send();
}

var html5QrCode = null;
var qrLoaded = false;

function loadQrLib(callback) {
    if (qrLoaded) { callback(); return; }
    var s = document.createElement('script');
    s.src = 'https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js';
    s.onload = function() { qrLoaded = true; callback(); };
    s.onerror = function() {
        // Fallback to another CDN
        var s2 = document.createElement('script');
        s2.src = 'https://cdn.jsdelivr.net/npm/html5-qrcode@2.3.8/dist/html5-qrcode.min.js';
        s2.onload = function() { qrLoaded = true; callback(); };
        s2.onerror = function() {
            document.getElementById('scanResult').textContent = '❌ 無法載入 QR 掃描庫';
        };
        document.head.appendChild(s2);
    };
    document.head.appendChild(s);
}

function startReader() {
    var result = document.getElementById('scanResult');
    var btn = document.getElementById('scanStartBtn');
    
    if (html5QrCode) {
        html5QrCode.stop().then(function(){
            html5QrCode.clear();
            html5QrCode = null;
            btn.textContent = '📷 掃描 QR Code';
            document.getElementById('reader').innerHTML = '';
            result.textContent = '';
        });
        return;
    }
    
    result.textContent = '📥 載入掃描器...';
    loadQrLib(function() {
        try {
            document.getElementById('reader').innerHTML = '';
            html5QrCode = new Html5Qrcode("reader");
            btn.textContent = '⏹ 關閉';
            result.textContent = '📷 對準 QR Code...';
            
            html5QrCode.start(
                { facingMode: "environment" },
                { fps: 10, qrbox: 250 },
                function(txt) {
                    // Success
                    html5QrCode.stop();
                    html5QrCode.clear();
                    html5QrCode = null;
                    btn.textContent = '📷 掃描 QR Code';
                    result.textContent = '✅ 已偵測！轉跳中...';
                    var url = txt;
                    if (url.indexOf('/wpay/pay/') >= 0 || url.indexOf('/wpay/') >= 0) {
                        setTimeout(function(){ window.location.href = url; }, 300);
                    } else if (url.indexOf('http') === 0 && url.indexOf('wbank.wtechhk.com') >= 0) {
                        setTimeout(function(){ window.location.href = url; }, 300);
                    } else {
                        result.innerHTML = '⚠️ 唔係付款碼<br><span style="font-size:11px;">已填入 Send</span>';
                        document.getElementById('wcoins-send-to').value = url;
                    }
                },
                function() {}
            ).catch(function(e) {
                result.textContent = '❌ ' + e.message;
                btn.textContent = '📷 掃描 QR Code';
                html5QrCode = null;
            });
        } catch(e) {
            result.textContent = '❌ ' + e.message;
            btn.textContent = '📷 掃描 QR Code';
        }
    });
function confirmScan() {
    if (!scannedUrl) { alert('未偵測到 QR Code'); return; }
    stopScanner();
    var url = scannedUrl;
    if (url.indexOf('/wpay/pay/') >= 0) {
        window.location.href = url;
    } else if (url.indexOf('http') === 0) {
        window.location.href = url;
    } else {
        document.getElementById('scanResult').textContent = '⚠️ 唔係有效付款碼: ' + url.slice(0,30);
    }
}

function sendWCoins() {
    var to = document.getElementById('wcoins-send-to').value.trim();
    var amt = document.getElementById('wcoins-send-amount').value.trim();
    var btn = document.getElementById('wcoins-send-btn');
    var result = document.getElementById('wcoins-send-result');
    if (!to || !amt || parseInt(amt) <= 0) { alert('Fill in receiver and amount'); return; }
    btn.disabled = true; btn.textContent = 'Processing...'; result.style.display = 'none';
    var x = new XMLHttpRequest();
    x.onreadystatechange = function() {
        if (x.readyState == 4) {
            try {
                var d = JSON.parse(x.responseText);
                if (d.success) {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">Sent ' + d.tx.amount + ' WCN to ' + d.tx.to + '<br><span style="font-size:12px;">Block #' + d.tx.block + '</span></div>';
                    document.getElementById('wcoins-send-to').value = '';
                    document.getElementById('wcoins-send-amount').value = '';
                    loadWCoinsInfo();
                } else {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">' + (d.error || 'Failed') + '</div>';
                }
            } catch(e) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Error</div>';
            }
            btn.disabled = false; btn.textContent = 'Send';
        }
    };
    x.open('POST', '/wcoins/api/send', true);
    x.setRequestHeader('Content-Type', 'application/json');
    x.send(JSON.stringify({receiver: to, amount: parseInt(amt)}));
}
// === Swap ===
var swapRate = {wtc:10, hkd:1, fee:10};
var swapDir = 'wtc'; // 'wtc' = WTC->HKD, 'hkd' = HKD->WTC

function setSwapDir(dir) {
    swapDir = dir;
    document.getElementById('swap-dir-wtc').style.background = dir === 'wtc' ? 'linear-gradient(135deg,#4fc3f7,#00bcd4)' : '#f1f5f9';
    document.getElementById('swap-dir-wtc').style.color = dir === 'wtc' ? '#0c0c1d' : '#64748b';
    document.getElementById('swap-dir-hkd').style.background = dir === 'hkd' ? 'linear-gradient(135deg,#4fc3f7,#00bcd4)' : '#f1f5f9';
    document.getElementById('swap-dir-hkd').style.color = dir === 'hkd' ? '#0c0c1d' : '#64748b';
    document.getElementById('swap-title').textContent = dir === 'wtc' ? 'Swap WTC to HKD' : 'Swap HKD to WTC';
    document.getElementById('swap-amount').placeholder = dir === 'wtc' ? 'WTC amount' : 'HKD amount';
    document.getElementById('swap-balance-label').innerHTML = 'WTC Balance: <b id="swap-wtc-bal">{{ balance }}</b>';
    document.getElementById('swap-hkd-label').innerHTML = 'HKD Available: <b id="swap-hkd-bal">${{ nowAmount }}</b>';
    // Clear preview
    document.getElementById('swap-preview').style.display = 'none';
    document.getElementById('swap-btn').disabled = true;
}

function loadSwapInfo() {
    var x = new XMLHttpRequest();
    x.onreadystatechange = function() {
        if (x.readyState == 4 && x.status == 200) {
            try { var d = JSON.parse(x.responseText);
            swapRate = d;
            document.getElementById('swap-rate').textContent = d.rate_label;
            document.getElementById('swap-fee').textContent = d.fee_label;
            } catch(e) {}
        }
    };
    x.open('GET', '/wbank/swap/info', true);
    x.send();
    
    var x2 = new XMLHttpRequest();
    x2.onreadystatechange = function() {
        if (x2.readyState == 4 && x2.status == 200) {
            try {
                var list = JSON.parse(x2.responseText);
                var el = document.getElementById('swap-history');
                if (!el) return;
                if (list.length === 0) { el.innerHTML = 'No swap history'; return; }
                var h = '';
                for (var i = 0; i < list.length; i++) {
                    var r = list[i];
                    h += '<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;display:flex;justify-content:space-between;">';
                    h += '<div><b>' + r.wtc_amount + ' WTC</b> → HK$' + r.amount + '</div>';
                    h += '<div>' + r.status + '</div></div>';
                }
                el.innerHTML = h;
            } catch(e) {}
        }
    };
    x2.open('GET', '/wbank/swap/history', true);
    x2.send();
}

function previewSwap() {
    var amt = document.getElementById('swap-amount').value;
    var preview = document.getElementById('swap-preview');
    var btn = document.getElementById('swap-btn');
    if (!amt || parseFloat(amt) <= 0) { preview.style.display = 'none'; btn.disabled = true; return; }
    if (swapDir === 'wtc') {
        var gross = amt * swapRate.hkd / swapRate.wtc;
        var fee = gross * (swapRate.fee_percent || 10) / 100;
        var net = gross - fee;
        document.getElementById('swap-receive-unit').textContent = 'HK$';
        document.getElementById('swap-fee-unit').textContent = 'HK$';
        document.getElementById('swap-net').textContent = net.toFixed(2);
        document.getElementById('swap-fee-amt').textContent = fee.toFixed(2);
    } else {
        var gross = amt * swapRate.wtc / swapRate.hkd;
        var fee = gross * (swapRate.fee_percent || 10) / 100;
        var net = gross - fee;
        document.getElementById('swap-receive-unit').textContent = 'WTC';
        document.getElementById('swap-fee-unit').textContent = 'WTC';
        document.getElementById('swap-net').textContent = net.toFixed(2);
        document.getElementById('swap-fee-amt').textContent = fee.toFixed(2);
    }
    preview.style.display = 'block';
    btn.disabled = false;
}

function applySwap() {
    var amt = parseFloat(document.getElementById('swap-amount').value);
    if (!amt || amt <= 0) return;
    var btn = document.getElementById('swap-btn');
    var result = document.getElementById('swap-result');
    btn.disabled = true; btn.textContent = 'Processing...'; result.style.display = 'none';
    var x = new XMLHttpRequest();
    x.onreadystatechange = function() {
        if (x.readyState == 4) {
            try {
                var d = JSON.parse(x.responseText);
                if (d.success) {
                    result.style.display = 'block';
                    if (d.direction === 'hkd_to_wtc') {
                        result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">Swapped HK$' + d.hkd_amount + ' → ' + d.wtc_amount + ' WTC<br>Fee: ' + d.fee_amount + ' WTC</div>';
                    } else {
                        result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">Swapped ' + d.wtc_amount + ' WTC → HK$' + d.net_hkd + '<br>Fee: HK$' + d.fee_hkd + '</div>';
                    }
                    document.getElementById('swap-amount').value = '';
                    document.getElementById('swap-preview').style.display = 'none';
                    loadSwapInfo();
                } else {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">' + (d.error || 'Failed') + '</div>';
                }
            } catch(e) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Error</div>';
            }
            btn.disabled = false; btn.textContent = 'Swap';
        }
    };
    x.open('POST', '/wbank/swap/apply', true);
    x.setRequestHeader('Content-Type', 'application/json');
    x.send(JSON.stringify({amount: amt, direction: swapDir}));
}


    // ===== Withdraw =====
    function toggleWithdrawFields() {
        var type = document.getElementById('withdraw-type').value;
        document.getElementById('withdraw-bank-fields').style.display = type === 'bank' ? 'block' : 'none';
        document.getElementById('withdraw-fps-fields').style.display = type === 'fps' ? 'block' : 'none';
    }

    function loadWithdrawInfo() {
        fetch('/wbank/withdraw/history').then(function(r){return r.json()}).then(function(list) {
            var el = document.getElementById('withdraw-history');
            if (!el) return;
            if (!list || list.length === 0) { el.innerHTML = '<div style="text-align:center;padding:30px 0;"><div style="font-size:40px;margin-bottom:10px;">📭</div><div style="color:#94a3b8;">No withdrawal requests</div></div>'; return; }
            var h = '';
            for (var i = 0; i < list.length; i++) {
                var r = list[i];
                var statusColor = r.status === 'approved' ? '#22c55e' : (r.status === 'rejected' ? '#ef4444' : '#f59e0b');
                var statusText = r.status === 'approved' ? 'Approved' : (r.status === 'rejected' ? 'Rejected' : 'Pending');
                var method = r.type === 'bank' ? r.bank_name + ' ' + r.account_number : 'FPS: ' + r.fps_account;
                h += '<div style="padding:10px;margin-bottom:8px;border-radius:10px;font-size:13px;background:#f8fafc;">';
                h += '<div style="display:flex;justify-content:space-between;align-items:center;">';
                h += '<div><b>HKD$' + r.amount + '</b><br><span style="font-size:11px;color:#64748b;">' + r.account_name + ' | ' + method + '</span></div>';
                h += '<div><span style="color:' + statusColor + ';font-weight:500;font-size:12px;">' + statusText + '</span><br><span style="font-size:10px;color:#94a3b8;">' + (r.time || '') + '</span></div></div></div>';
            }
            el.innerHTML = h;
        }).catch(function(){});
    }

    function applyWithdraw() {
        var type = document.getElementById('withdraw-type').value;
        var amount = parseFloat(document.getElementById('withdraw-amount').value);
        var btn = document.getElementById('withdraw-btn');
        var result = document.getElementById('withdraw-result');
        if (!amount || amount <= 0) { alert('Enter amount'); return; }
        var data = {amount: amount, type: type};
        if (type === 'bank') {
            data.bank_name = document.getElementById('withdraw-bank-name').value.trim();
            data.account_name = document.getElementById('withdraw-account-name').value.trim();
            data.account_number = document.getElementById('withdraw-account-number').value.trim();
            if (!data.bank_name || !data.account_name || !data.account_number) { alert('Fill bank details'); return; }
        } else {
            data.fps_account = document.getElementById('withdraw-fps-account').value.trim();
            data.account_name = document.getElementById('withdraw-fps-name').value.trim();
            if (!data.fps_account || !data.account_name) { alert('Fill FPS details'); return; }
        }
        btn.disabled = true; btn.textContent = 'Processing...'; result.style.display = 'none';
        fetch('/wbank/withdraw/apply', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(function(r){return r.json()}).then(function(d) {
            if (d.success) {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">Withdrawal request submitted for HKD$' + d.amount + '</div>';
                document.getElementById('withdraw-amount').value = '';
                loadWithdrawInfo();
            } else {
                result.style.display = 'block';
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">' + (d.error || 'Failed') + '</div>';
            }
            btn.disabled = false; btn.textContent = 'Submit Withdraw';
        }).catch(function(e) {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Error</div>';
            btn.disabled = false; btn.textContent = 'Submit Withdraw';
        });
    }


    // ===== Settings =====
    function loadSettingsInfo() {}

    function changePassword() {
        var oldPw = document.getElementById('settings-old-pw').value;
        var newPw = document.getElementById('settings-new-pw').value;
        var confirmPw = document.getElementById('settings-confirm-pw').value;
        var result = document.getElementById('settings-pw-result');
        if (!oldPw || !newPw) { alert('Fill all fields'); return; }
        if (newPw !== confirmPw) { alert('Passwords do not match'); return; }
        if (newPw.length < 6) { alert('Password too short (min 6 chars)'); return; }
        fetch('/wbank/settings/change_password', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({old_password: oldPw, new_password: newPw})
        }).then(function(r){return r.json()}).then(function(d) {
            result.style.display = 'block';
            if (d.success) {
                result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">Password updated successfully</div>';
                document.getElementById('settings-old-pw').value = '';
                document.getElementById('settings-new-pw').value = '';
                document.getElementById('settings-confirm-pw').value = '';
            } else {
                result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">' + (d.error || 'Failed') + '</div>';
            }
        }).catch(function(e) {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Error</div>';
        });
    }

    function toggleMFA() {
        var enabled = document.getElementById('settings-mfa-toggle').checked;
        fetch('/wbank/settings/toggle_mfa', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({enabled: enabled})
        }).then(function(r){return r.json()}).then(function(d) {
            if (d.success) {
                document.getElementById('settings-mfa').textContent = enabled ? 'Enabled' : 'Disabled';
            }
        }).catch(function(){});
    }
}