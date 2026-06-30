f=open('main.py','rb')  
lines=f.readlines()  
f.close()  
for i in range(570, 585):  
    s=lines[i].decode('utf-8').rstrip()  
    if s.strip(): print('L'+str(i+1)+': '+s)  
