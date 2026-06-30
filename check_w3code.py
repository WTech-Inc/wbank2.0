import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
print(f'Size: {len(w3)} bytes')
print(f'Has ERC20 transfer: {"ERC20 WTC Transfer" in w3}')
print(f'Has WTC_CONFIG: {"WTC_CONTRACT_ADDRESS" in w3}')
print(f'Has web3_bp: {"web3_bp" in w3}')
print(f'Has login check: {"is_authenticated" in w3}')
print(f'Has pytz: {"import pytz" in w3}')

# Check if the web3_bp is registered in main.py
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
print(f'\nmain.py:')
print(f'Has web3_bp register: {"register_blueprint(web3_bp)" in m}')
print(f'Has from wbank_web3 import: {"from wbank_web3" in m or "import wbank_web3" in m}')
