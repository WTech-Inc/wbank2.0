"""Find tx-history element in template"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# Find tx-history
idx = tpl.find('tx-history')
if idx >= 0:
    print(f'Found at position {idx}:')
    print(tpl[idx-100:idx+500])
    print()

# Also find the send section
idx2 = tpl.find('send-result')
if idx2 >= 0:
    print(f'send-result at {idx2}:')
    print(tpl[idx2-100:idx2+200])
