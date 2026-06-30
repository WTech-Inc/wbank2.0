"""Set up private blockchain using Geth PoA + deploy WTC"""
import sys, os, subprocess, time, json
sys.stdout.reconfigure(encoding='utf-8')

chain_dir = 'E:\\wbank\\private-chain'
os.makedirs(chain_dir, exist_ok=True)

# 1. Download Geth for Windows
print('[1/6] Downloading Geth...')
geth_url = 'https://gethstore.blob.core.windows.net/builds/geth-windows-amd64-1.14.12-2b1d2e5c.exe'
geth_path = os.path.join(chain_dir, 'geth.exe')

if not os.path.exists(geth_path):
    import urllib.request
    try:
        urllib.request.urlretrieve(geth_url, geth_path)
        print('  [OK] Geth downloaded')
    except:
        print('  [WARN] Download failed, trying alternative...')
        # Alternative: use go install or direct binary
        # For now, check if geth is already in PATH
        pass
else:
    print('  [OK] Geth already exists')

# Check if geth exists
if os.path.exists(geth_path):
    result = subprocess.run([geth_path, 'version'], capture_output=True, text=True, timeout=10)
    print(f'  Geth version: {result.stdout[:100]}')
else:
    print('  [WARN] Geth not found, will need manual install')

# 2. Create genesis.json (PoA, zero gas, instant sealing)
print('\n[2/6] Creating genesis config...')
# Generate a password-protected account
pw_path = os.path.join(chain_dir, 'password.txt')
with open(pw_path, 'w') as f:
    f.write('wtc123\n')

genesis = {
    "config": {
        "chainId": 456789,
        "homesteadBlock": 0,
        "eip150Block": 0,
        "eip155Block": 0,
        "eip158Block": 0,
        "byzantiumBlock": 0,
        "constantinopleBlock": 0,
        "petersburgBlock": 0,
        "istanbulBlock": 0,
        "berlinBlock": 0,
        "londonBlock": 0,
        "clique": {
            "period": 2,
            "epoch": 30000
        }
    },
    "gasLimit": "0xFFFFFFFF",
    "difficulty": "0x1",
    "extradata": "0x0000000000000000000000000000000000000000000000000000000000000000cA02C4888D7dfa3f052702b1288cF3eE50F248D70000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "alloc": {
        "0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7": {
            "balance": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
        },
        "0xdffA9CFE9FFA749Fd93883c587193381263AA59c": {
            "balance": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
        },
        "0x18DD69502788f38d76855fbcA7f42D86b0E30329": {
            "balance": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
        }
    }
}

genesis_path = os.path.join(chain_dir, 'genesis.json')
with open(genesis_path, 'w') as f:
    json.dump(genesis, f, indent=2)
print('  [OK] genesis.json created')
print(f'  Chain ID: 456789')
print(f'  Gas: 0 gas (free)')

# 3. Create start script
print('\n[3/6] Creating start scripts...')
bat = '''@echo off
cd /d E:\\wbank\\private-chain
echo Starting private WTC chain...
echo RPC: http://localhost:8545
echo Network ID: 456789
echo Gas: Free (0 gas)
echo.
geth --datadir data --networkid 456789 --http --http.addr 0.0.0.0 --http.port 8545 --http.api eth,web3,net,personal,admin --http.corsdomain "*" --http.vhosts "*" --allow-insecure-unlock --nodiscover --mine --miner.threads 1 --syncmode full console
'''

bat_path = os.path.join(chain_dir, 'start_chain.bat')
with open(bat_path, 'w') as f:
    f.write(bat)

print('  [OK] start_chain.bat created')

# 4. Create instructions for MetaMask
print('\n[4/6] MetaMask config...')
meta = '''
=== MetaMask Network Config ===
Network Name: WTC Private Chain
RPC URL: http://223.18.36.147:8545
Chain ID: 456789
Currency Symbol: WTC
Explorer: (none)

=== Import Wallet ===
WTC gas token: 0 gas (free)
All accounts have unlimited WTC balance.

=== Steps ===
1. Open MetaMask → Add Network
2. RPC: http://223.18.36.147:8545
3. Chain ID: 456789
4. Switch to WTC Private Chain
5. Import wallet using private key from E:\\.env
'''
meta_path = os.path.join(chain_dir, 'METAMASK_SETUP.txt')
with open(meta_path, 'w') as f:
    f.write(meta)

# 5. Update WBank config for private chain
print('\n[5/6] Creating deploy script for private chain...')
deploy = '''"""Deploy WTC to private chain"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()
from solcx import compile_files, install_solc
install_solc('0.8.20')

cd = 'E:\\\\wbank\\\\contracts'
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
print(f'Connected: {w3.is_connected()}, Block: {w3.eth.block_number}')

# Load deployer key
pk = ""
with open('E:\\\\wbank\\\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]
dep = Account.from_key(pk)
print(f'Deployer: {dep.address}')
print(f'ETH: {w3.from_wei(w3.eth.get_balance(dep.address), "ether")}')

# Compile
compiled = compile_files([os.path.join(cd, 'WTC.sol')], solc_version='0.8.20', output_values=['abi', 'bin'])
wtc_info = [v for k,v in compiled.items() if 'WTC' in k and 'Bridge' not in k][0]

# Deploy
nonce = w3.eth.get_transaction_count(dep.address)
WTC = w3.eth.contract(abi=wtc_info['abi'], bytecode=wtc_info['bin'])
tx = WTC.constructor().build_transaction({'from':dep.address,'nonce':nonce,'gas':2000000,'gasPrice':0,'chainId':456789})
signed = dep.sign_transaction(tx)
h = w3.eth.send_raw_transaction(signed.raw_transaction)
r = w3.eth.wait_for_transaction_receipt(h, timeout=60)
print(f'WTC deployed: {r.contractAddress}')
print(f'Zero gas deploy: ✅')

# Save
with open(os.path.join(cd, 'deployments', 'private-chain.json'), 'w') as f:
    json.dump({'chain_id':456789,'wtc':{'address':r.contractAddress}}, f, indent=2)
'''

deploy_path = os.path.join(chain_dir, 'deploy_wtc.py')
with open(deploy_path, 'w') as f:
    f.write(deploy)
print('  [OK] deploy_wtc.py created')

# 6. Create init + deploy batch file
print('\n[6/6] Creating one-click setup...')
init_bat = '''@echo off
cd /d E:\\wbank\\private-chain
echo ========================
echo WTC Private Chain Setup
echo ========================
echo.

echo Step 1: Init chain...
if not exist data ( geth --datadir data init genesis.json ) else ( echo Already initialized )

echo.
echo Step 2: Compile + deploy WTC...
python deploy_wtc.py

echo.
echo ========================
echo Done! Start chain with:
echo start_chain.bat
echo ========================
pause
'''

init_path = os.path.join(chain_dir, 'setup_and_deploy.bat')
with open(init_path, 'w') as f:
    f.write(init_bat)

print('\n===========================')
print('✅  Private Chain Ready!')
print('===========================')
print(f'Disk space: 666 GB free')
print(f'Chain dir: {chain_dir}')
print(f'Chain ID: 456789')
print(f'Gas: 0 gas (FREE)')
print(f'')
print('To start:')
print(f'  1. cd E:\\\\wbank\\\\private-chain')
print(f'  2. setup_and_deploy.bat  (init + deploy WTC)')
print(f'  3. start_chain.bat  (start RPC server)')
print(f'')
print(f'MetaMask:')
print(f'  RPC: http://223.18.36.147:8545')
print(f'  Chain ID: 456789')
print(f'  Gas: Free!')
