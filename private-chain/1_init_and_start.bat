@echo off
cd /d E:\wbank\private-chain
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
