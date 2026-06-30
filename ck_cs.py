with open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

sections = []
for i, line in enumerate(lines):
    s = line.strip()
    if 'id=' in s and ('page' in s or 'Modal' in s or 'screen' in s or 'Screen' in s):
        sections.append((i+1, s[:100]))
    elif 'class="page"' in s or 'class="nav-item"' in s:
        sections.append((i+1, s[:100]))
    elif 'class="nav"' in s and ('nav-item' in s or 'nav' not in s):
        pass

print('=== Pages/Screens ===')
for line, text in sections:
    print(f'  L{line}: {text}')
