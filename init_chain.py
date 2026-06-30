"""Init private chain with simple genesis"""
import sys, os, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')

chain_dir = 'E:\\wbank\\private-chain'
os.makedirs(chain_dir, exist_ok=True)

# Simple genesis
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
        "clique": {"period": 1, "epoch": 30000}
    },
    "extraData": "0x" + "0"*64 + "cA02C4888D7dfa3f052702b1288cF3eE50F248D7" + "0"*130,
    "gasLimit": "0xE0000000",
    "difficulty": "0x1",
    "alloc": {
        "0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7": {"balance": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"},
        "0xdffA9CFE9FFA749Fd93883c587193381263AA59c": {"balance": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"},
        "0x18DD69502788f38d76855fbcA7f42D86b0E30329": {"balance": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"}
    }
}

g_path = os.path.join(chain_dir, 'genesis.json')
with open(g_path, 'w') as f:
    json.dump(genesis, f, indent=2)
print('[OK] genesis.json written')

# Init
geth = os.path.join(chain_dir, 'geth.exe')
data_dir = os.path.join(chain_dir, 'data')

result = subprocess.run([geth, '--datadir', data_dir, 'init', g_path],
    capture_output=True, text=True, timeout=30)
print(f'Init RC: {result.returncode}')
print(f'Out: {result.stdout[:300]}')
print(f'Err: {result.stderr[:300]}')

if result.returncode == 0:
    print('[OK] Chain initialized!')
else:
    print('[FAIL] Init failed')

# Update start script
start_bat = '''@echo off
cd /d E:\\wbank\\private-chain
ECHO Starting WTC Private Chain...
ECHO RPC: http://0.0.0.0:8545
ECHO ChainID: 456789
ECHO Gas: FREE
ECHO.
geth.exe --datadir data ^
  --networkid 456789 ^
  --http --http.addr 0.0.0.0 --http.port 8545 ^
  --http.api eth,web3,net,txpool,personal,admin ^
  --http.corsdomain "*" --http.vhosts "*" ^
  --nodiscover ^
  --mine --miner.etherbase 0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7 ^
  --allow-insecure-unlock --rpc.allow-unprotected-txs ^
  --syncmode full --gcmode archive
'''

with open(os.path.join(chain_dir, 'start.bat'), 'w') as f:
    f.write(start_bat)
print('[OK] start.bat written')
