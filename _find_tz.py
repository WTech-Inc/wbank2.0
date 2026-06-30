f=open('wcoins_blockchain.py','rb')  
lines=f.readlines()  
f.close()  
for i,l in enumerate(lines):  
    s=l.decode('utf-8').rstrip()  
    if 'strftime' in s or 'utcnow' in s or 'created_at' in s or 'datetime' in s:  
        print('L'+str(i+1)+': '+s)  
