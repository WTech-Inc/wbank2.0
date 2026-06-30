import sys  
with open('main.py','rb') as f:  
    lines = f.readlines()  
for i in range(228,400):  
    print(f'L{i+1}: {lines[i].decode("utf-8").rstrip()}')  
