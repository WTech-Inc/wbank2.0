# Fix wbankClient.html template - remove investment features and 泓國 references
import sys

path = 'E:\\wbank\\templates\\wbankClient.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)
changes = []

# 1. Remove tradeChart nav button
old = '<div class="nav-item" onclick="showPage(\'tradeChart\')">投資</div>'
if old in content:
    content = content.replace(old, '')
    changes.append('nav button')
else:
    print('WARN: nav button not found')

# 2. Fix 泓國稅務局 -> 稅務局
if '泓國稅務局' in content:
    content = content.replace('泓國稅務局', '稅務局')
    changes.append('泓國稅務局')

# 3. Fix 泓國南省政府 -> 南省政府
if '泓國南省政府' in content:
    content = content.replace('泓國南省政府', '南省政府')
    changes.append('泓國南省政府')

# 4. Remove tradeChart page section
start_marker = '<div id="tradeChart" class="page">'
end_marker = '<div id="trade" class="page">'
start_idx = content.find(start_marker)
end_idx = content.find(end_marker)
if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
    content = content[:start_idx] + content[end_idx:]
    changes.append('tradeChart page')
else:
    print(f'WARN: tradeChart section not found ({start_idx}, {end_idx})')

# 5. Remove stock JavaScript section (from //Stock place to // Chat UI)
js_start = content.find('//Stock place')
js_end = content.find('// Chat UI')
if js_start != -1 and js_end != -1 and js_end > js_start:
    content = content[:js_start] + content[js_end:]
    changes.append('stock JS')
else:
    print(f'WARN: stock JS section not found ({js_start}, {js_end})')

# 6. Remove investment setInterval and init calls
old2 = 'setInterval(()=>{\n     Object.keys(stockPrices).forEach(stock => randomPriceChange(stock));\n   },5000)\n   updateBalance(); // 初始化餘額\n   renderPortfolio(); // 插然投資組合'
if old2 in content:
    content = content.replace(old2, '')
    changes.append('setInterval')
else:
    print('WARN: setInterval block not found (might use different encoding)')

# Clean up leftover empty lines
content = content.replace('\n\n\n\n\n', '\n\n')
content = content.replace('\n\n\n\n', '\n\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Changes made: {len(changes)} items - {changes}')
print(f'Size: {original_len} -> {len(content)} bytes')
