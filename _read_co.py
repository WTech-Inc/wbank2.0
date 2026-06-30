f=open('main.py','rb')  
lines=f.readlines()  
f.close()  
for i in range(3300,3330):  
    l=lines[i].decode('utf-8').rstrip()  
    if l.strip():  
        print('L'+str(i+1)+': '+l)  
