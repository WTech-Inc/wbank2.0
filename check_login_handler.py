import sys
sys.stdout.reconfigure(encoding='utf-8')
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
idx = m.find('def wbank_v1_auth_session')
if idx >= 0:
    print(m[idx:idx+600])
