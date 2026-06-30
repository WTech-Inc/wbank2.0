"""Fix swap JS field name mismatch and duplicates"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/wbankClient.html"
c = open(path, "r", encoding="utf-8").read()

# Fix fee_percent references
c = c.replace("swapRate.fee / 100", "swapRate.fee_percent / 100")

# Fix d.fee_percent -> swapRate.fee_percent (d not in scope)
c = c.replace("document.getElementById('swap-fee-pct').textContent = d.fee_percent;",
              "document.getElementById('swap-fee-pct').textContent = swapRate.fee_percent;")

# Remove duplicate swap JS section (everything between first and last copy)
# Count how many swap JS blocks exist
count = c.count("function loadSwapInfo")
print(f"Found {count} loadSwapInfo functions")

if count > 1:
    # Find first occurrence
    first = c.find("function loadSwapInfo")
    # Find the start of the section (the comment before it)
    section_start = c.rfind("// === WTC/HKD Swap ===", 0, first)
    if section_start < 0:
        section_start = first
    # Find last occurrence
    last = c.rfind("function loadSwapInfo")
    last_end = c.find("// Auto load web3", last)
    if last_end < 0:
        last_end = c.find("</script>", last)

    # Remove all but last
    before = c[:section_start]
    after = c[last_end:]
    c = before + after
    print("Removed duplicate swap JS sections")

# Also fix the apply endpoint error (handle HTML responses)
old_apply = '''                const d = await r.json();
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
                }'''

new_apply = '''                const text = await r.text();
                let d;
                try { d = JSON.parse(text); } catch(e) {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">Server error, please try again</div>';
                    btn.disabled = false; btn.innerHTML = 'Apply Swap';
                    return;
                }
                if (d.success) {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">' +
                        'Swap successful!<br>' +
                        '<b>' + d.wtc_amount + ' WTC</b> → <b>HK$' + d.net_hkd + '</b><br>' +
                        '<span style="font-size:12px;">Rate: ' + d.rate + ' | Fee: HK$' + d.fee_hkd + '</span>' +
                        '</div>';
                    document.getElementById('swap-amount').value = '';
                    document.getElementById('swap-preview').style.display = 'none';
                    try { const b = await fetch('/wbank/web3/info'); const bd = await b.json();
                        if (bd.balance !== undefined && document.getElementById('main-balance'))
                            document.getElementById('main-balance').textContent = bd.balance; } catch(e) {}
                    loadSwapInfo();
                } else {
                    result.style.display = 'block';
                    result.innerHTML = '<div style="background:#fef2f2;color:#dc2626;padding:12px;border-radius:8px;">' + (d.error || 'Swap failed') + '</div>';
                }'''

c = c.replace(old_apply, new_apply)

open(path, "w", encoding="utf-8").write(c)
print(f"Saved ({len(c)} bytes)")
