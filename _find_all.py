f=open('main.py','rb')  
lines=f.readlines()  
f.close()  
for i in range(len(lines)):  
    line=lines[i].decode('utf-8').rstrip()  
    if 'def ' in line and 'wcoins' in line.lower():  
        print('L'+str(i+1)+': '+line)  
for i in range(len(lines)):  
    line=lines[i].decode('utf-8').rstrip()  
    if '@app.route' in line.lower() and 'wcoins' in line.lower():  
        print('L'+str(i+1)+': '+line)  
