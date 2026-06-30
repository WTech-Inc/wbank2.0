import sys
sys.stdout.reconfigure(encoding='utf-8')
tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()
print('Has loadWeb3Info:', 'loadWeb3Info' in tpl)
print('Has error text:', '請先登入' in tpl or 'Not logged in' in tpl)
print('Has tx-history:', 'tx-history' in tpl)
print('Size:', len(tpl))
print('Has sendWTC:', 'sendWTC' in tpl)
