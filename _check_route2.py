f=open('main.py','rb')  
lines=f.readlines()  
f.close()  
for i in range(579, 590):  
    print(str(i+1)+': '+lines[i].decode('utf-8').rstrip())  
