"""Fix wbankClient.html - swap click bug and improve wallet tx UX"""
import re

f = open('templates/wbankClient.html', 'r', encoding='utf-8')
c = f.read()
f.close()

# Fix 1: Remove the broken onclick override (replaces showPage with just loadSwapInfo)
c = re.sub(
    r"// Update showPage to load swap info\nvar oldLoadSwap = setTimeout;\ndocument\.querySelector\('\[onclick\*=\\'swap\\'\]'\)\.onclick = function\(\) \{ setTimeout\(loadSwapInfo, 100\); \};\n",
    '',
    c
)

# Fix 2: Remove duplicate setTimeout for swap
c = c.replace(
    "if (id === 'swap') setTimeout(loadSwapInfo, 100);\n        if (id === 'swap') setTimeout(loadSwapInfo, 100);",
    "if (id === 'swap') setTimeout(loadSwapInfo, 100);"
)

# Fix 3: Check if 'swap-page' in CSS - add any missing styling
if '.swap-container' not in c:
    print('swap-container not found in CSS')

# Fix 4: Improve wallet tx-history UX
old_tx_html = '''                var list = txns && txns.transactions || [];
                if (list.length === 0) { el.innerHTML = 'No transactions'; return; }
                var h = '';
                for (var i = 0; i < list.length; i++) {
                    var tx = list[i];
                    var icon = tx.type === 'sent' ? '↗' : '↙';
                    var color = tx.type === 'sent' ? '#ef4444' : '#4ade80';
                    var other = tx.type === 'sent' ? tx.receiver : tx.sender;
                    h += '<div style="padding:10px 0;border-bottom:1px solid #f1f5f9;font-size:12px;display:flex;justify-content:space-between;align-items:center;">';
                    h += '<div><span>' + icon + '</span> <b>' + tx.amount + '</b> WCN<br>';
                    h += '<span style="color:#94a3b8;">' + (tx.type==='sent'?'To: ':'From: ') + other + '</span></div>';
                    h += '<div style="text-align:right;color:' + color + ';">#' + tx.block_index + '<br>';
                    h += '<span style="color:#94a3b8;font-size:10px;">' + (tx.created_at || '') + '</span></div></div>';
                }'''

new_tx_html = '''                var list = txns && txns.transactions || [];
                if (list.length === 0) { el.innerHTML = '<div style="text-align:center;padding:30px 0;"><div style="font-size:40px;margin-bottom:10px;">📭</div><div style="color:#94a3b8;">No transactions yet</div></div>'; return; }
                var h = '';
                for (var i = 0; i < list.length; i++) {
                    var tx = list[i];
                    var isSent = tx.type === 'sent';
                    var icon = isSent ? '↗' : '↙';
                    var color = isSent ? '#ef4444' : '#22c55e';
                    var bgColor = isSent ? '#fef2f2' : '#f0fdf4';
                    var other = isSent ? tx.receiver : tx.sender;
                    var otherLabel = isSent ? 'To' : 'From';
                    var shortOther = other.length > 15 ? other.slice(0,6)+'...'+other.slice(-4) : other;
                    var time = tx.created_at || '';
                    if (time.length > 10) time = time.slice(0, 16);
                    h += '<div style="padding:10px;margin-bottom:8px;border-radius:8px;font-size:13px;display:flex;justify-content:space-between;align-items:center;background:'+bgColor+';">';
                    h += '<div style="display:flex;align-items:center;gap:10px;">';
                    h += '<div style="width:36px;height:36px;border-radius:50%;background:'+color+';color:white;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:bold;">'+icon+'</div>';
                    h += '<div><div style="font-weight:600;color:#1e293b;">'+tx.amount+' WCN</div>';
                    h += '<div style="color:#64748b;font-size:11px;">'+otherLabel+': '+shortOther+'</div></div></div>';
                    h += '<div style="text-align:right;"><div style="font-size:11px;font-weight:500;color:'+color+';">#'+tx.block_index+'</div>';
                    h += '<div style="color:#94a3b8;font-size:10px;">'+time+'</div></div></div>';
                }'''

if old_tx_html in c:
    c = c.replace(old_tx_html, new_tx_html)
    print('Improved wallet tx UX')
else:
    print('WARNING: old_tx_html pattern not found!')
    # Try to find a portion of it
    if 'tx.type === ' in c:
        idx = c.index("tx.type === ")
        print(f'  Found at position {idx}, context: ...{c[idx:idx+100]}...')

f = open('templates/wbankClient.html', 'w', encoding='utf-8')
f.write(c)
f.close()
print('Template updated successfully')
