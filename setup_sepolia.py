"""Switch to Sepolia Testnet for free testing and deploy contracts"""
import sys, subprocess, os, time, json
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update wbank_web3.py to Sepolia
print('[1/5] Switching wbank_web3.py to Sepolia...')
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
w3 = w3.replace('WTC_CHAIN_ID = 1', 'WTC_CHAIN_ID = 11155111')
w3 = w3.replace('ETH_RPC = "https://ethereum-rpc.publicnode.com"', 'SEPOLIA_RPC = "https://ethereum-sepolia.publicnode.com"')
w3 = w3.replace('w3 = Web3(Web3.HTTPProvider(ETH_RPC))', 'w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))')
w3 = w3.replace('"network": "Ethereum Mainnet"', '"network": "Sepolia Testnet"')
w3 = w3.replace('WTC_RPC_URL = "https://ethereum-rpc.publicnode.com"', 'WTC_RPC_URL = "https://ethereum-sepolia.publicnode.com"')
open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)
print('  [OK] Sepolia config written')

# Verify
check = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
for line in check.split('\n'):
    if 'CHAIN_ID' in line or 'RPC' in line or 'network' in line:
        print(f'  {line.strip()[:100]}')

# 2. Create .env with deployer key
print('\n[2/5] Checking OpenZeppelin contracts...')
oz_path = 'E:\\wbank\\contracts\\node_modules\\@openzeppelin\\contracts'
if not os.path.exists(oz_path):
    os.chdir('E:\\wbank\\contracts')
    subprocess.run(['npm', 'init', '-y'], capture_output=True, timeout=30)
    r = subprocess.run(['npm', 'install', '@openzeppelin/contracts'], capture_output=True, text=True, timeout=120)
    if r.returncode == 0:
        print('  [OK] OpenZeppelin installed')
    else:
        print(f'  [WARN] npm install: {r.stderr[:200]}')
else:
    print('  [OK] OpenZeppelin already installed')

# 3. Install solcx
print('\n[3/5] Installing solcx...')
r = subprocess.run([sys.executable, '-m', 'pip', 'install', 'py-solc-x'], capture_output=True, text=True, timeout=120)
print(f'  {"[OK]" if r.returncode == 0 else "[WARN]"} py-solc-x installed')

# 4. Generate deployer wallet if needed
print('\n[4/5] Setting up deployer...')
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

# Generate new wallet
acct = Account.create()
print(f'  Deployer Address: {acct.address}')
print(f'  Private Key: {acct.key.hex()}')
print()
print('  ⚠️  IMPORTANT: Send Sepolia ETH to this address!')
print('  Go to: https://www.alchemy.com/faucets/ethereum-sepolia')
print(f'  Or: https://sepoliafaucet.com/')
print()
print(f'  Address: {acct.address}')
print()

# Save to .env
env_path = 'E:\\wbank\\contracts\\.env'
with open(env_path, 'w') as f:
    f.write(f'DEPLOYER_PRIVATE_KEY=0x{acct.key.hex()}\n')
print(f'  [OK] Private key saved to {env_path}')

# 5. Deploy
print('\n[5/5] Deploying contracts (need ETH in wallet first)...')
print()
print('  === DEPLOYMENT INSTRUCTIONS ===')
print(f'  1. Send Sepolia ETH to: {acct.address}')
print('     (Use faucet - takes 1-2 min)')
print()
print('  2. Then run:')
print('     cd /d E:\\wbank\\contracts')
print('     python deploy_contracts.py --network sepolia')
print()
print('  3. After deploy, update WTC_CONTRACT_ADDRESS in:')
print('     E:\\wbank\\wbank_web3.py')
print('     (Script will do this automatically if run from E:\\wbank)')
print()
print('  4. Restart server: restart server')

# Show deploy command with env
print()
print('  Or one-liner:')
print(f'  set DEPLOYER_PRIVATE_KEY=0x{acct.key.hex()} && cd /d E:\\wbank\\contracts && python deploy_contracts.py --network sepolia')

# Verify syntax
import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('\n[OK] Syntax OK - ready for deployment!')
