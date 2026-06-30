import os
os.chdir('E:/wbank')
files = ['templates/wbank/createUser.html', 'templates/wbank/kyc.html']
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    changed = 0
    for i, line in enumerate(lines):
        if '泓國' in line:
            lines[i] = line.replace('泓國', '')
            changed += 1
    with open(f, 'w', encoding='utf-8') as fh:
        fh.writelines(lines)
    print(f'Fixed {changed} references in {f}')

print('DONE')
