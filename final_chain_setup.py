"""Create final chain startup files for user to run manually"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

cd = 'E:\\wbank\\private-chain'

# 1. Simple genesis
genesis = {
    "config": {"chainId": 456789, "homesteadBlock": 0, "eip150Block": 0, "eip155Block": 0, "eip158Block": 0, "byzantiumBlock": 0, "constantinopleBlock": 0, "petersburgBlock": 0, "istanbulBlock": 0, "berlinBlock": 0, "londonBlock": 0, "clique": {"period": 1, "epoch": 30000}},
    "extraData": "0x" + "0"*64 + "cA02C4888D7dfa3f052702b1288cF3eE50F248D7" + "0"*130,
    "gasLimit": "0xE0000000",
    "difficulty": "0x1",
    "alloc": {
        "0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7": {"balance": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"},
        "0xdffA9CFE9FFA749Fd93883c587193381263AA59c": {"balance": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"}
    }
}

with open(os.path.join(cd, 'genesis.json'), 'w', encoding='utf-8') as f:
    json.dump(genesis, f, indent=2)
print('[OK] genesis.json')

# 2. Simple init + start batch
init_bat = '''@echo off
cd /d E:\\wbank\\private-chain
echo ===================================
echo   WTC Private Chain 初始化
echo ===================================
echo.
echo Step 1: 初始化區塊鏈...
geth.exe --datadir data init genesis.json
if errorlevel 1 goto error
echo [OK] 初始化完成
echo.
echo Step 2: 啟動區塊鏈節點...
echo RPC: http://localhost:8545
echo ChainID: 456789
echo Gas: Free!
echo.
echo 啟動中，請稍候...
start "WTC-Chain" cmd /c "geth.exe --datadir data --networkid 456789 --http --http.addr 0.0.0.0 --http.port 8545 --http.api eth,web3,net,personal --http.corsdomain * --http.vhosts * --nodiscover --mine --miner.etherbase 0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7 --allow-insecure-unlock --syncmode full"
echo [OK] 節點已啟動
echo.
echo ===================================
echo  啟動完成！
echo  到 MetaMask 加入：
echo  RPC: http://223.18.36.147:8545
echo  ChainID: 456789
echo ===================================
pause
goto end
:error
echo [FAIL] 初始化失敗
pause
:end
'''

with open(os.path.join(cd, '1_init_and_start.bat'), 'w', encoding='utf-8') as f:
    f.write(init_bat)
print('[OK] 1_init_and_start.bat')

# 3. Deploy WTC batch
deploy_bat = '''@echo off
cd /d E:\\wbank\\private-chain
echo ===================================
echo   部署 WTC Token
echo ===================================
echo.
echo 請確保節點已在運行 (第1步已做)
echo.
python deploy_wtc.py
echo.
pause
'''

with open(os.path.join(cd, '2_deploy_wtc.bat'), 'w', encoding='utf-8') as f:
    f.write(deploy_bat)
print('[OK] 2_deploy_wtc.bat')

# 4. README
with open(os.path.join(cd, 'README.txt'), 'w', encoding='utf-8') as f:
    f.write('''WTC Private Chain - Setup Guide
================================

E: Drive Free Space: 666 GB
Chain ID: 456789
Gas: FREE (0 gas)

HOW TO SETUP:
===============

STEP 1: Initialize + Start Chain
  Double-click: 1_init_and_start.bat
  - This will init the chain and start the node
  - Keep the cmd window open (it's the node)
  - RPC will be at http://localhost:8545

STEP 2: Deploy WTC Token
  Double-click: 2_deploy_wtc.bat
  - Deploys WTC token to your private chain

STEP 3: MetaMask
  Network Name: WTC Private Chain
  RPC URL: http://223.18.36.147:8545
  Chain ID: 456789
  Currency Symbol: WTC

YOUR ACCOUNTS (have unlimited balance):
  0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7
  0xdffA9CFE9FFA749Fd93883c587193381263AA59c

NOTES:
  - Private chain is only accessible when the CMD window is open
  - If you close the window, the chain stops
  - All balances prefunded, all gas is FREE
''')

print(f'\nAll files created in: {cd}')
print('1. Double-click: 1_init_and_start.bat')
print('2. Then: 2_deploy_wtc.bat')
print('3. MetaMask: RPC http://223.18.36.147:8545 | ChainID 456789')
