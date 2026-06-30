import sys  
f=open('templates/wbankClient.html','rb')  
lines=f.readlines()  
f.close()  
for i in range(len(lines)):  
    s=lines[i].decode('utf-8').rstrip()  
    if 'swap' in s.lower():  
        print('L'+str(i+1)+': '+s[:200])  
