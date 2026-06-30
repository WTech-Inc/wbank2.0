"""Rename deployer to wcoins.banker in .env and wbank_web3.py"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Update .env
env_path = 'E:/wbank/.env'
env = open(env_path, 'r').read()
env = env.replace('DEPLOYER_PRIVATE_KEY', 'WCOINS_BANKER_PRIVATE_KEY')
open(env_path, 'w').write(env)
print('OK - .env: WCOINS_BANKER_PRIVATE_KEY')

# Update wbank_web3.py
w3_path = 'E:/wbank/wbank_web3.py'
w3src = open(w3_path, 'r', encoding='utf-8').read()

old = "if _l.startswith('DEPLOYER_PRIVATE_KEY='):"
new = "if _l.startswith('WCOINS_BANKER_PRIVATE_KEY=') or _l.startswith('DEPLOYER_PRIVATE_KEY='):"

if old in w3src:
    w3src = w3src.replace(old, new)
    open(w3_path, 'w', encoding='utf-8').write(w3src)
    print('OK - wbank_web3.py updated')
else:
    print('Pattern not found in wbank_web3.py')
    # Debug - show what's there
    idx = w3src.find('DEPLOYER')
    if idx >= 0:
        print('Found:', w3src[idx:idx+80])
    else:
        print('DEPLOYER not found in file')
