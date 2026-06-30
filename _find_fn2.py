f=open('wbank_web3.py','rb')  
lines=f.readlines()  
f.close()  
for i,l in enumerate(lines):  
    l=l.decode('utf-8').rstrip()  
    if '@app.route' in l or '@wbank.route' in l or '@bp.route' in l or '@web3.route' in l:  
        print('L'+str(i+1)+': '+l)  
