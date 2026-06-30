"""Complete private chain setup with proper configs"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

chain_dir = 'E:\\wbank\\private-chain'
os.makedirs(chain_dir, exist_ok=True)

# Correct extradata for Clique PoA (signer = deployer address)
# Format: 32 zero bytes + signer address (no 0x) + 65 zero bytes
signer = 'cA02C4888D7dfa3f052702b1288cF3eE50F248D7'
extradata = '0x' + '0'*64 + signer + '0'*130

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
            "period": 0,
            "epoch": 30000
        }
    },
    "nonce": "0x0",
    "timestamp": "0x0",
    "extraData": extradata,
    "gasLimit": "0xE0000000",
    "difficulty": "0x1",
    "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "coinbase": "0x0000000000000000000000000000000000000000",
    "alloc": {
        "0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7": {"balance": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"},
        "0xdffA9CFE9FFA749Fd93883c587193381263AA59c": {"balance": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"},
        "0x18DD69502788f38d76855fbcA7f42D86b0E30329": {"balance": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"}
    },
    "number": "0x0",
    "gasUsed": "0x0",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000"
}

with open(os.path.join(chain_dir, 'genesis.json'), 'w', encoding='utf-8') as f:
    json.dump(genesis, f, indent=2)

# Create start script
bat = '''@echo off
cd /d E:\\wbank\\private-chain
echo ===================================
echo   WTC Private Chain
echo   RPC: http://0.0.0.0:8545
echo   Chain ID: 456789
echo   Gas: FREE (0)
echo ===================================
echo.
geth.exe --datadir data init genesis.json
geth.exe --datadir data ^
  --networkid 456789 ^
  --http --http.addr 0.0.0.0 --http.port 8545 ^
  --http.api eth,web3,net,txpool,personal,admin ^
  --http.corsdomain "*" --http.vhosts "*" ^
  --nodiscover --mine --miner.etherbase 0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7 ^
  --allow-insecure-unlock --rpc.allow-unprotected-txs ^
  --syncmode full
'''

with open(os.path.join(chain_dir, 'start.bat'), 'w', encoding='utf-8') as f:
    f.write(bat)

# Deploy script for private chain
deploy = '''import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()
from solcx import compile_files, install_solc
install_solc("0.8.20")

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
print(f"Connected: {w3.is_connected()}, Block: {w3.eth.block_number}")

pk = ""
with open("E:\\\\wbank\\\\.env") as f:
    for line in f:
        line = line.strip()
        if line.startswith("DEPLOYER_PRIVATE_KEY="):
            pk = line.split("=", 1)[1].strip()
            break
if pk.startswith("0x"): pk = pk[2:]
dep = Account.from_key(pk)
print(f"Deployer: {dep.address}")

cd = "E:\\\\wbank\\\\contracts"
compiled = compile_files([os.path.join(cd, "WTC.sol")], solc_version="0.8.20", output_values=["abi", "bin"])
wtc_info = [v for k,v in compiled.items() if "WTC" in k and "Bridge" not in k][0]

nonce = w3.eth.get_transaction_count(dep.address)
WTC = w3.eth.contract(abi=wtc_info["abi"], bytecode=wtc_info["bin"])
tx = WTC.constructor().build_transaction({"from":dep.address,"nonce":nonce,"gas":2000000,"gasPrice":0,"chainId":456789})
signed = dep.sign_transaction(tx)
h = w3.eth.send_raw_transaction(signed.raw_transaction)
r = w3.eth.wait_for_transaction_receipt(h, timeout=120)
print(f"WTC deployed: {r.contractAddress} (gas used: {r.gasUsed}, gas price: 0)")

os.makedirs(os.path.join(cd, "deployments"), exist_ok=True)
with open(os.path.join(cd, "deployments", "private-chain.json"), "w") as f:
    json.dump({"chain_id":456789,"wtc":{"address":r.contractAddress}}, f, indent=2)
print("Done!")
'''

with open(os.path.join(chain_dir, 'deploy_wtc.py'), 'w', encoding='utf-8') as f:
    f.write(deploy)

# MetaMask instructions
readme = '''
==================================
WTC Private Chain Setup Guide
==================================

E: drive space: 666 GB free
Chain directory: E:\\wbank\\private-chain
Chain ID: 456789
Gas: FREE (0 gas)

==================================
Step 1: Download Geth
==================================
1. Download from: https://geth.ethereum.org/downloads/
2. Choose "Windows" version
3. Extract geth.exe to: E:\\wbank\\private-chain\\

==================================
Step 2: Start Chain
==================================
Open CMD as Administrator:
  cd /d E:\\wbank\\private-chain
  start.bat

==================================
Step 3: Deploy WTC Token
==================================
Open ANOTHER CMD:
  cd /d E:\\wbank\\private-chain
  python deploy_wtc.py

==================================
Step 4: MetaMask
==================================
Network Name: WTC Private Chain
RPC URL: http://223.18.36.147:8545
Chain ID: 456789
Currency Symbol: WTC

Import Account with Private Key from:
  E:\\.env (DEPLOYER_PRIVATE_KEY)
'''

with open(os.path.join(chain_dir, 'README.txt'), 'w', encoding='utf-8') as f:
    f.write(readme)

print('Private chain setup complete!')
print(f'Location: {chain_dir}')
print(f'Chain ID: 456789')
print(f'Gas: 0 (free)')
print(f'Disk free: 666 GB')
print(f'\nTo complete:')
print(f'1. Download geth.exe from https://geth.ethereum.org/downloads/')
print(f'   Save to: {chain_dir}\\geth.exe')
print(f'2. Run: start.bat')
print(f'3. Run: python deploy_wtc.py')
print(f'4. MetaMask: RPC http://223.18.36.147:8545  ChainID 456789')
