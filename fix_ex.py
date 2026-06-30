d = open('E:\\wbank\\templates\\wbank.html', 'r', encoding='utf-8').read()

# Find the stats-row div and add exchange rate
old = '''            <div class="stat-card">
                <div class="num"><span class="counter" data-target="99">0</span>.9%</div>
                <div class="lbl">系統正常運行</div>
            </div>
        </div>'''

new = '''            <div class="stat-card">
                <div class="num"><span class="counter" data-target="99">0</span>.9%</div>
                <div class="lbl">系統正常運行</div>
            </div>
            <div class="stat-card">
                <div class="num">WTC$10</div>
                <div class="lbl">= HKD$1（官方匯率）</div>
            </div>
        </div>'''

if old in d:
    d = d.replace(old, new)
    open('E:\\wbank\\templates\\wbank.html', 'w', encoding='utf-8').write(d)
    print('Exchange rate added')
else:
    print('Could not find target text')
    idx = d.find('系統正常運行')
    if idx >= 0:
        print(f'Found at {idx}, context: {d[idx-50:idx+100]}')
