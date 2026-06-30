import os, glob

os.chdir('E:/wbank')
found = []
for f in glob.glob('**/*.html', recursive=True):
    try:
        d = open(f, 'r', encoding='utf-8').read()
        if '泓國' in d:
            found.append(f)
    except:
        pass
for f in glob.glob('**/*.py', recursive=True):
    try:
        d = open(f, 'r', encoding='utf-8').read()
        if '泓國' in d:
            found.append(f)
    except:
        pass
print('Found 泓國 in:', found if found else 'NONE')
