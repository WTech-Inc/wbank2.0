"""Fix socket.io script tag - separate from inline JS"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()
old = '<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.js">'
new = '<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.js"><' + '/script>\n    <script>'

if old in tpl:
    tpl = tpl.replace(old, new)
    open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8').write(tpl)
    print('[OK] SocketIO script separated')
else:
    print('[WARN] Pattern not found')

# Verify
check = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()
s1 = 'socket.io.js">'
s2 = 'socket.io.js"></scrip' + 't>'
print(f's1 count: {check.count(s1)}')
print(f's2 count: {check.count(s2)}')
print(f'loadWeb3Info count: {check.count("function loadWeb3Info")}')
