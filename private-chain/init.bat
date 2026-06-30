@echo off
cd /d E:\wbank\private-chain
echo Init chain...
E:\wbank\private-chain\geth.exe --datadir E:\wbank\private-chain\data init E:\wbank\private-chain\genesis.json
echo EXIT CODE: %ERRORLEVEL%
if exist E:\wbank\private-chain\data\geth\chaindata (
  echo SUCCESS: Chain initialized
) else (
  echo FAIL: Chain not initialized
)
pause
