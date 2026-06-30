import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Find and fix the wbankwallet creation in register_submit
old = '''        nu = wbankwallet(username=u, password=pw, email=em,
            accnumber="WB"+str(int(_time.time()))[-8:],
            balance="0", role="user", sub="active", verify="pending")'''

new = '''        nu = wbankwallet(username=u, password=pw, email=em,
            accnumber="WB"+str(int(_time.time()))[-8:],
            balance="0", role="user", sub="active", verify="pending",
            openpay=False, setamount=0, nowamount=0)'''

if old in m:
    m = m.replace(old, new)
    print('[OK] Fixed wbankwallet constructor')
else:
    print('[WARN] Could not find pattern')
    # Show context
    idx = m.find('nu = wbankwallet')
    if idx >= 0:
        print(f'Found at position {idx}:')
        print(m[idx:idx+300])
    else:
        print('Not found at all')

open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('[OK] Syntax OK')
except py_compile.PyCompileError as e:
    print(f'[FAIL] {e}')
