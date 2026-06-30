"""Read exact get_chain source"""
import sys
f = open('wcoins_blockchain.py', 'rb')
lines = f.readlines()
f.close()
for i in range(113, 128):
    print(str(i+1) + ': ' + lines[i].decode('utf-8').rstrip())
