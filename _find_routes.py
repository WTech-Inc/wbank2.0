import sys  
f=open('wbank_web3.py','rb')  
lines=f.readlines()  
f.close()  
for i in range(len(lines)):  
    line=lines[i].decode('utf-8').rstrip()  
    if '.route' in line or 'def ' in line:  
        print('L'+str(i+1)+': '+line)  
