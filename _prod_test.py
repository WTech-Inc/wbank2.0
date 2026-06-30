import urllib.request, json  
hdr = {'User-Agent': 'Mozilla/5.0'}  
base = 'https://wbank.wtechhk.com'  
tests = [  
    ('GET', '/wbank/swap/info', None),  
    ('GET', '/wbank/swap/history', None),  
    ('POST', '/wbank/swap/apply', json.dumps({'amount':10}).encode()),  
    ('GET', '/admin/api/swaps', None),  
    ('GET', '/admin_swap', None),  
]  
for method, path, body in tests:  
    try:  
        req = urllib.request.Request(base+path, data=body, headers=hdr, method=method)  
        r = urllib.request.urlopen(req, timeout=10)  
        print(str(r.status)+' '+path+' ('+str(len(r.read()))+' bytes)')  
    except Exception as e:  
        print('ERR '+path+': '+str(e))  
