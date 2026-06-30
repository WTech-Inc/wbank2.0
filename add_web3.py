with open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Web3 nav item after the myPage nav item
old_nav = '''        <div class="nav-item" onclick="showPage('myPage')">我的</div>'''
new_nav = '''        <div class="nav-item" onclick="showPage('myPage')">我的</div>
        <div class="nav-item" onclick="showPage('web3')">Web3</div>'''
content = content.replace(old_nav, new_nav)

# 2. Add Web3 page section before the Confirm Screen
old_confirm = '''        <!-- Confirm Screen -->
        <div id="allConfirmModal" class="modal">'''

web3_section = '''        <!-- Web3 Wallet Page -->
        <div id="web3" class="page">
            <div class="card">
                <div style="text-align:center;margin-bottom:20px;">
                    <div style="font-size:48px;margin-bottom:10px;">🔗</div>
                    <h2 style="background:linear-gradient(135deg,#4fc3f7,#00bcd4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">WTC ERC20 Token</h2>
                    <p style="color:gray;font-size:14px;">WCoins - Ethereum ERC20</p>
                </div>

                <div style="background:linear-gradient(135deg,#1a1a3e,#0c0c1d);border-radius:12px;padding:20px;margin-bottom:16px;color:white;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                        <span style="font-size:14px;color:rgba(255,255,255,0.5);">WTC Balance</span>
                        <span style="background:rgba(79,195,247,0.2);padding:4px 12px;border-radius:12px;font-size:12px;color:#4fc3f7;">ERC20</span>
                    </div>
                    <div style="font-size:36px;font-weight:bold;">WTC$<span id="web3-balance">{{ balance }}</span></div>
                    <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-top:4px;">≈ HKD${{ "%.2f"|format(balance|int / 10) }}</div>
                </div>

                <div style="background:white;border:1px solid #e8ecf1;border-radius:12px;padding:16px;margin-bottom:16px;">
                    <label style="font-size:12px;color:#94a3b8;display:block;margin-bottom:6px;">Wallet Address (ERC20)</label>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <input type="text" id="web3-address" value="0x{{ hash_card_number[:40] }}" readonly
                               style="flex:1;padding:10px;border:1px solid #e2e8f0;border-radius:8px;font-size:13px;font-family:monospace;background:#f8fafc;color:#1a1a2e;">
                        <button onclick="copyAddress()" style="padding:10px 16px;background:#1a1a2e;color:white;border:none;border-radius:8px;cursor:pointer;font-size:13px;">Copy</button>
                    </div>
                </div>

                <div style="text-align:center;margin-bottom:16px;">
                    <p style="font-size:13px;color:#94a3b8;margin-bottom:10px;">掃描 QR Code 接收 WTC</p>
                    <div style="display:inline-block;background:white;padding:16px;border-radius:12px;border:1px solid #e8ecf1;">
                        <img src="data:image/svg+xml;base64,{{ img }}" alt="ERC20 Receive QR" width="220" height="220">
                    </div>
                    <p style="font-size:11px;color:#94a3b8;margin-top:8px;">只發送 WTC (ERC20) 到此地址</p>
                </div>

                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;">
                    <div style="background:#f8fafc;border-radius:8px;padding:12px;text-align:center;">
                        <div style="font-size:11px;color:#94a3b8;">Token Name</div>
                        <div style="font-size:14px;font-weight:600;color:#1a1a2e;">WCoins</div>
                    </div>
                    <div style="background:#f8fafc;border-radius:8px;padding:12px;text-align:center;">
                        <div style="font-size:11px;color:#94a3b8;">Symbol</div>
                        <div style="font-size:14px;font-weight:600;color:#1a1a2e;">WTC</div>
                    </div>
                    <div style="background:#f8fafc;border-radius:8px;padding:12px;text-align:center;">
                        <div style="font-size:11px;color:#94a3b8;">Decimals</div>
                        <div style="font-size:14px;font-weight:600;color:#1a1a2e;">18</div>
                    </div>
                    <div style="background:#f8fafc;border-radius:8px;padding:12px;text-align:center;">
                        <div style="font-size:11px;color:#94a3b8;">Network</div>
                        <div style="font-size:14px;font-weight:600;color:#1a1a2e;">Ethereum</div>
                    </div>
                </div>

                <div style="background:#fff8e1;border:1px solid #ffe082;border-radius:8px;padding:12px;margin-bottom:16px;">
                    <p style="font-size:12px;color:#f57f17;margin:0;">
                        ⚠️ WTC (WCoins) 是基於 Ethereum ERC20 標準的數位代幣。
                        請確保只發送 WTC 到此地址，發送其他代幣可能導致資產損失。
                    </p>
                </div>
            </div>
        </div>

'''

content = content.replace(old_confirm, web3_section + '\n' + old_confirm)

# 3. Add Web3 JavaScript in the script section (before the closing </script>)
old_script_end = '</script>'
web3_js = '''
        // === Web3 Wallet ===
        function copyAddress() {
            const addr = document.getElementById('web3-address');
            addr.select();
            addr.setSelectionRange(0, 99999);
            navigator.clipboard.writeText(addr.value).then(() => {
                alert('地址已複製: ' + addr.value);
            }).catch(() => {
                document.execCommand('copy');
                alert('地址已複製');
            });
        }
        // Check if MetaMask is installed
        if (typeof window.ethereum !== 'undefined') {
            console.log('MetaMask detected!');
        }
'''

content = content.replace(old_script_end, web3_js + '\n' + old_script_end)

with open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Web3 section added to user panel')
