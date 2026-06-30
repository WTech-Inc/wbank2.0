import os, glob
os.chdir('E:/wbank')

files = list(glob.glob('**/*.py', recursive=True)) + list(glob.glob('**/*.html', recursive=True))
issues = []

for f in files:
    try:
        d = open(f, 'r', encoding='utf-8').read()
    except:
        continue
    if '泓國' in d:
        issues.append(f'{f} - has 泓國')
    if 'FLASK_ADMIN' in d:
        issues.append(f'{f} - has FLASK_ADMIN')

if issues:
    for i in issues:
        print(i)
else:
    print('ALL CLEAN - no remaining issues')

# Verify key changes
print()
main = open('main.py', 'r', encoding='utf-8').read()
print('write_audit_log in main.py:', 'write_audit_log' in main)
print('/admin/dashboard in main.py:', '/admin/dashboard' in main)
print('audit_log in models.py:', 'audit_log' in open('models.py', 'r', encoding='utf-8').read())
print('admin/index.html exists:', os.path.exists('templates/admin/index.html'))
cli = open('templates/wbankClient.html', 'r', encoding='utf-8').read()
print('tradeChart in client.html:', 'tradeChart' in cli)
print('Stock place in client.html:', 'Stock place' in cli)
