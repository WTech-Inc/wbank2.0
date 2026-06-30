"""Check the web3 frontend HTML for issues"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# Find web3 section
idx = tpl.find('id="web3"')
if idx > 0:
    print('=== Web3 tab content ===')
    print(tpl[idx:idx+3000])
else:
    print('No id="web3" found')

# Find tx-history
print('\n=== tx-history container ===')
idx2 = tpl.find('tx-history')
if idx2 > 0:
    print(tpl[idx2-200:idx2+300])

# Check if wbankrecord model exists
print('\n=== Checking models ===')
mod = open('E:\\wbank\\models.py', 'r', encoding='utf-8').read()
if 'class wbankrecord' in mod:
    print('wbankrecord model found')
else:
    print('wbankrecord model NOT in models.py')
    # Check if it's in main.py
    main = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
    if 'class wbankrecord' in main:
        print('wbankrecord model IS in main.py')
    else:
        print('wbankrecord model NOT found anywhere')
