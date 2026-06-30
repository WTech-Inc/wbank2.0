"""Fix login handler to accept active users"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
old = "if user.sub == None or user.sub == \"\":"
new = "if user.sub == None or user.sub == \"\" or user.sub == \"active\":"
if old in m:
    m = m.replace(old, new)
    open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)
    print('Fixed login handler')
else:
    print('Pattern not found')
