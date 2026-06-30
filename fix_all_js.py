"""Find and fix ALL JS issues in wbankClient.html"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# Find all inline script blocks
scripts = list(re.finditer(r'<script>(.*?)</script>', tpl, re.DOTALL))
print(f'Found {len(scripts)} inline script blocks')

# Check for showPage definition
showpage_defined = False
showpage_overridden = False
for i, m in enumerate(scripts):
    code = m.group(1)
    if 'function showPage(' in code:
        showpage_defined = True
        print(f'Block {i}: showPage defined')
    if 'showPage = function' in code and 'const _orig' in code:
        showpage_overridden = True
        print(f'Block {i}: showPage overridden')

print(f'showPage defined: {showpage_defined}')
print(f'showPage overridden: {showpage_overridden}')

# The issue is clear: the earlier script blocks have syntax errors
# This prevents showPage from being defined
# Solution: Remove ALL inline scripts and regenerate clean ones

# But that's too complex. Instead, let's find the first syntax error
# by checking each block

for i, m in enumerate(scripts):
    code = m.group(1)
    # Remove strings for better balance check
    no_strings = re.sub(r"'[^']*'", '', code)
    no_strings = re.sub(r'"[^"]*"', '', no_strings)
    no_strings = re.sub(r'//[^\n]*', '', no_strings)
    bal = no_strings.count('{') - no_strings.count('}')
    if bal != 0:
        lines = code.split('\n')
        # Find where balance goes wrong
        line_bal = 0
        for j, line in enumerate(lines):
            stripped = re.sub(r"'[^']*'", '', line)
            stripped = re.sub(r'"[^"]*"', '', stripped)
            stripped = re.sub(r'//.*', '', stripped)
            line_bal += stripped.count('{') - stripped.count('}')
            if abs(line_bal) > 50:  # Way too many braces
                print(f'Block {i}, line {j}: balance={line_bal}')
                print(f'  {line.strip()[:100]}')

# Strategy: Replace the ENTIRE script section with clean code
# Find all script content between first <script> and last </script>
first_script = tpl.find('<script>')
last_script = tpl.rfind('</script>')
if last_script < 0:
    last_script = tpl.rfind('</SCRIPT>')

if first_script >= 0 and last_script > first_script:
    # Get everything before and after script section
    before = tpl[:first_script]
    after = tpl[last_script + 9:]  # len('</script>') = 9

    # Build clean consolidated scripts
    clean_scripts = '''<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.js"></script>
<script>
// ===== MAIN APPLICATION SCRIPTS =====

function showPage(pageId) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    const el = document.getElementById(pageId);
    if (el) el.classList.add('active');
}

// ===== CORE FUNCTIONS =====
const buy = () => { window.open('/wbank/action?type=buy'); };
const sell = () => { window.open('/wbank/action?type=sell'); };
const moneyScreen = () => { window.open('/wbank/action?type=money'); };
const closeMoneyScreen = () => {};
const openSettingScreen = () => { window.open('/wbank/action?type=settings'); };
const closeScreenScreen = () => {};
const removeAcc = () => { window.open('/wbank/action?type=remove'); };
const paymentNeed = () => { window.open('/wbank/action?type=payment'); };
const closeResult = () => {};
const closeRecord = () => {};
const closeNfc = () => {};

// ===== Web3 Wallet =====
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
            histContainer.innerHTML = '<p style="color:#94a3b8;text-align:center;padding:20px;">\\u66AB\\u7121\\u4EA4\\u6613\\u8A18\\u9304</p>';
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
    if (!to || !amt) { alert('\\u8ACB\\u586B\\u5BEB\\u63A5\\u6536\\u5730\\u5740\\u548C\\u6578\\u91CF'); return; }
    if (!to.startsWith('0x') || to.length !== 42) { alert('\\u8ACB\\u8F38\\u5165\\u6709\\u6548\\u7684\\u5730\\u5740'); return; }
    if (parseInt(amt) <= 0) { alert('\\u6578\\u91CF\\u5FC5\\u9808\\u5927\\u65BC 0'); return; }
    btn.disabled = true; btn.innerHTML = '\\u23f3 \\u8655\\u7406\\u4E2D...'; result.style.display = 'none';
    try {
        const r = await fetch('/wbank/web3/send', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({to, amount: parseInt(amt)}) });
        const d = await r.json();
        if (d.success) {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">\\u2705 \\u6210\\u529F\\u767C\\u9001 ' + d.amount + ' WTC<br>TX: ' + (d.tx_hash ? d.tx_hash.slice(0,20)+'...' : '') + '</div>';
            try { const b = await fetch('/wbank/web3/info'); const bd = await b.json(); if (bd.balance !== undefined && document.getElementById('web3-balance')) document.getElementById('web3-balance').textContent = bd.balance; } catch(e) {}
            loadWeb3Info();
        } else {
            result.style.display = 'block';
            result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">\\u274c ' + (d.error || '\\u767C\\u9001\\u5931\\u6557') + '</div>';
        }
    } catch(e) {
        result.style.display = 'block';
        result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">\\u274c ' + (e.message || '\\u7DB2\\u8DEF\\u932F\\u8AA4') + '</div>';
    }
    btn.disabled = false; btn.innerHTML = '\\ud83d\\udd17 \\u767C\\u9001 WTC';
}

// Load web3 info on web3 tab
showPage = (function(orig) {
    return function(id) {
        if (orig) orig(id);
        if (id === 'web3') setTimeout(loadWeb3Info, 200);
    };
})(typeof showPage === 'function' ? showPage : null);
</script>'''

    new_tpl = before + clean_scripts + after

    with open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8') as f:
        f.write(new_tpl)

    print(f'[OK] Replaced {len(scripts)} script blocks with clean version')
    print('[OK] File size:', len(new_tpl), 'bytes')
    print('[OK] Restart server')
else:
    print('[ERR] Could not find script boundaries')
