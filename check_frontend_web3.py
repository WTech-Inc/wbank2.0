"""Check the frontend web3 JavaScript code"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# Find the web3 JavaScript section
idx = tpl.find('// === Web3 Wallet ===')
if idx >= 0:
    print(tpl[idx:idx+2000])
else:
    print('Web3 Wallet section not found')
    # Search for web3 related JS
    for keyword in ['loadWeb3Info', 'sendWTC', 'web3-info', 'web3-address', 'tx-history']:
        print(f'{keyword}: {keyword in tpl}')
