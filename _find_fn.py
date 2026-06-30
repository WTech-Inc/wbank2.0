f=open('main.py','rb')  
lines=f.readlines()  
f.close()  
for i in range(len(lines)):  
    l=lines[i].decode('utf-8').rstrip()  
    if '@app.route' in l and 'swap' in l:  
        print('L'+str(i+1)+': '+l)  
