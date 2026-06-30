f=open('main.py','rb')  
lines=f.readlines()  
f.close()  
for i in range(395,450):  
    l=lines[i].decode('utf-8').rstrip()  
    if l.strip():  
        print(str(i+1)+': '+l)  
