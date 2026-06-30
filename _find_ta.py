f=open('main.py','rb')  
lines=f.readlines()  
f.close()  
for i in range(len(lines)):  
    line=lines[i].decode('utf-8').rstrip()  
    if 'trade_wcoins' in line or '@app.route.*swap' in line or 'def .*swap' in line:  
        print('L'+str(i+1)+': '+line)  
