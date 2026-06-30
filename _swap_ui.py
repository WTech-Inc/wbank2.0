import sys  
f=open('templates/wbankClient.html','rb')  
lines=f.readlines()  
f.close()  
for i in range(100, 140):  
    s=lines[i].decode('utf-8').rstrip()  
    try:  
        if s.strip(): print('L'+str(i+1)+': '+s)  
    except:  
        print('L'+str(i+1)+': '+repr(s))  
