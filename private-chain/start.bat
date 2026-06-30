@echo off
cd /d E:\wbank\private-chain
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
