"""Clean up duplicate web3 JS in wbankClient.html - keep only ONE version"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# Find the CORRECT loadWeb3Info (the one with proper error handling)
# Find the section between first // === Web3 Wallet === and the function before it ends
# Strategy: Find all "// === Web3 Wallet ===" sections and keep only the LAST one

# First, let's find ALL script blocks
scripts = []
idx = 0
while True:
    start = tpl.find('// === Web3 Wallet ===', idx)
    if start < 0:
        break
    # Find the end of this section - next similar marker or significant change
    end = tpl.find('// ===', start + 20)
    if end < 0:
        end = len(tpl)
    scripts.append((start, end))
    idx = end

print(f'Found {len(scripts)} Web3 Wallet sections')

if len(scripts) > 1:
    # Keep only the LAST one (which should have all the fixes)
    last_start, last_end = scripts[-1]

    # Keep everything before the first section
    first_start = scripts[0][0]
    before = tpl[:first_start]

    # Keep only the last section
    web3_js = tpl[last_start:last_end]

    # Keep everything after the last section
    after = tpl[last_end:]

    # But we need to keep ALL non-duplicate HTML too
    # The issue is the sections might be spread throughout the file
    # Let's take a different approach: remove duplicate lines/patterns

    # Count occurrences of key functions
    for fn in ['loadWeb3Info', 'sendWTC', 'copyAddress']:
        count = tpl.count(f'async function {fn}')
        print(f'  {fn}: {count} occurrences')

# Alternative: Just write the clean web3 section
print('\n=== Regenerating clean web3 JS ===')

# Find the LAST occurrence of each function
last_load = tpl.rfind('async function loadWeb3Info')
last_send = tpl.rfind('async function sendWTC')
last_show = tpl.rfind('showPage = function')

# Extract the clean versions
load_fn_end = tpl.find('\n        }\n', last_load)
if load_fn_end > 0:
    load_fn_end = tpl.find('\n', load_fn_end + 1)
    clean_load = tpl[last_load:load_fn_end]

send_fn_end = tpl.find('\n        }\n\n', last_send)
if send_fn_end > 0:
    send_fn_end = tpl.find('\n', send_fn_end + 1)
    clean_send = tpl[last_send:send_fn_end]

show_fn_end = tpl.find('\n        }\n', last_show)
if show_fn_end > 0:
    show_fn_end = tpl.find('\n', show_fn_end + 1)
    clean_show = tpl[last_show:show_fn_end]

print(f'loadWeb3Info: {len(clean_load)} chars' if 'clean_load' in dir() else 'not found')
print(f'sendWTC: {len(clean_send)} chars' if 'clean_send' in dir() else 'not found')
print(f'showPage: {len(clean_show)} chars' if 'clean_show' in dir() else 'not found')

# Now build the clean template
# Starting from the original, remove ALL "// === Web3 Wallet ===" sections
# and replace with one clean version

# Remove all sections between markers
clean = re.sub(
    r'// === Web3 Wallet ===.*?// === Web3 Wallet ===',
    '// === Web3 Wallet ===\n',
    tpl,
    flags=re.DOTALL
)

# The above removes everything between markers, leaving just "// === Web3 Wallet ==="
# Now we need to add our clean JS after it

# Find the marker
marker_pos = clean.find('// === Web3 Wallet ===')
if marker_pos >= 0:
    # Find the next blank line after the marker (where old code ended)
    end_of_section = clean.find('\n\n', marker_pos)
    if end_of_section < 0:
        end_of_section = clean.find('\n        }\n', marker_pos)
        if end_of_section > 0:
            end_of_section = clean.find('\n', end_of_section + 1)

    # Get all the clean functions
    clean_code = '\n        // === Web3 Wallet Functions ===\n'
    clean_code += '        async function loadWeb3Info() {\n'
    clean_code += '            const addrField = document.getElementById(\'web3-address\');\n'
    clean_code += '            const histContainer = document.getElementById(\'tx-history\');\n'
    clean_code += '            const balanceField = document.getElementById(\'web3-balance\');\n'
    clean_code += '            try {\n'
    clean_code += '                const r = await fetch(\'/wbank/web3/info\');\n'
    clean_code += '                const d = await r.json();\n'
    clean_code += '                if (d.error) {\n'
    clean_code += '                    if (addrField) addrField.value = \'請先登入\';\n'
    clean_code += '                    if (histContainer) histContainer.innerHTML = \'<p style="color:#ef4444;text-align:center;padding:20px;">⚠️ \' + d.error + \'</p>\';\n'
    clean_code += '                    return;\n'
    clean_code += '                }\n'
    clean_code += '                if (d.address && addrField) addrField.value = d.address;\n'
    clean_code += '                if (d.balance !== undefined && balanceField) balanceField.textContent = d.balance;\n'
    clean_code += '            } catch(e) { console.log(\'Web3:\', e); }\n'
    clean_code += '            try {\n'
    clean_code += '                const r2 = await fetch(\'/wbank/web3/history\');\n'
    clean_code += '                const txns = await r2.json();\n'
    clean_code += '                if (!histContainer) return;\n'
    clean_code += '                if (txns && txns.error) {\n'
    clean_code += '                    histContainer.innerHTML = \'<p style="color:#ef4444;text-align:center;padding:20px;">⚠️ \' + txns.error + \'</p>\';\n'
    clean_code += '                    return;\n'
    clean_code += '                }\n'
    clean_code += '                if (!txns || txns.length === 0) {\n'
    clean_code += '                    histContainer.innerHTML = \'<p style="color:#94a3b8;text-align:center;padding:20px;">暫無交易記錄</p>\';\n'
    clean_code += '                } else {\n'
    clean_code += '                    histContainer.innerHTML = txns.map(t =>\n'
    clean_code += '                        \'<div style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">\' +\n'
    clean_code += '                        \'<span style="color:#1a1a2e;">\' + (t.action || \'\') + \'</span><br>\' +\n'
    clean_code += '                        \'<span style="color:#94a3b8;">\' + (t.time || \'\') + \'</span></div>\'\n'
    clean_code += '                    ).join(\'\');\n'
    clean_code += '                }\n'
    clean_code += '            } catch(e) { console.log(\'History:\', e); }\n'
    clean_code += '        }\n\n'
    clean_code += '        async function sendWTC() {\n'
    clean_code += '            const to = document.getElementById(\'send-to\').value.trim();\n'
    clean_code += '            const amount = document.getElementById(\'send-amount\').value.trim();\n'
    clean_code += '            const btn = document.getElementById(\'send-btn\');\n'
    clean_code += '            const result = document.getElementById(\'send-result\');\n'
    clean_code += '            if (!to || !amount) { alert(\'請填寫接收地址和數量\'); return; }\n'
    clean_code += '            if (!to.startsWith(\'0x\') || to.length !== 42) { alert(\'請輸入有效的 Ethereum 地址 (0x...)\'); return; }\n'
    clean_code += '            if (parseInt(amount) <= 0) { alert(\'數量必須大於 0\'); return; }\n'
    clean_code += '            btn.disabled = true; btn.innerHTML = \'⏳ 處理中...\'; result.style.display = \'none\';\n'
    clean_code += '            try {\n'
    clean_code += '                const r = await fetch(\'/wbank/web3/send\', {\n'
    clean_code += '                    method: \'POST\',\n'
    clean_code += '                    headers: {\'Content-Type\': \'application/json\'},\n'
    clean_code += '                    body: JSON.stringify({to: to, amount: parseInt(amount)})\n'
    clean_code += '                });\n'
    clean_code += '                const d = await r.json();\n'
    clean_code += '                if (d.success) {\n'
    clean_code += '                    result.style.display = \'block\';\n'
    clean_code += '                    result.innerHTML = \'<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">\' + \'✅ 成功發送 \' + d.amount + \' WTC<br>TX: \' + (d.tx_hash ? d.tx_hash.slice(0, 20) + \'...\' : \'\') + \'</div>\';\n'
    clean_code += '                    try { const b = await fetch(\'/wbank/web3/info\'); const bd = await b.json(); if (bd.balance !== undefined && document.getElementById(\'web3-balance\')) document.getElementById(\'web3-balance\').textContent = bd.balance; } catch(e) {}\n'
    clean_code += '                    loadWeb3Info();\n'
    clean_code += '                } else {\n'
    clean_code += '                    result.style.display = \'block\';\n'
    clean_code += '                    result.innerHTML = \'<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ \' + (d.error || \'發送失敗\') + \'</div>\';\n'
    clean_code += '                }\n'
    clean_code += '            } catch(e) {\n'
    clean_code += '                result.style.display = \'block\';\n'
    clean_code += '                result.innerHTML = \'<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">❌ 錯誤: \' + (e.message || \'網絡錯誤\') + \'</div>\';\n'
    clean_code += '            }\n'
    clean_code += '            btn.disabled = false; btn.innerHTML = \'🔗 發送 WTC\';\n'
    clean_code += '        }\n\n'
    clean_code += '        function copyAddress() {\n'
    clean_code += '            const addr = document.getElementById(\'web3-address\');\n'
    clean_code += '            if (addr) { addr.select(); document.execCommand(\'copy\'); alert(\'地址已複製\'); }\n'
    clean_code += '        }\n\n'
    clean_code += '        // Load web3 info on tab switch\n'
    clean_code += '        const origShowPage = showPage;\n'
    clean_code += '        showPage = function(pageId) {\n'
    clean_code += '            if (origShowPage) origShowPage(pageId);\n'
    clean_code += '            if (pageId === \'web3\') setTimeout(loadWeb3Info, 100);\n'
    clean_code += '        };\n'
    clean_code += '        // === END Web3 Wallet ===\n'

    clean = clean[:marker_pos] + clean_code + clean[end_of_section+1:]

    # Write back
    with open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8') as f:
        f.write(clean)

    print(f'[OK] Clean web3 JS written ({len(clean_code)} chars)')
    print(f'[OK] File size: {len(clean)} bytes')

print('\n=== Restart server ===')
