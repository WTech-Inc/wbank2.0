@echo off
cd /d E:\wbank\private-chain
echo Starting WTC Private Chain...
echo RPC: http://localhost:8545
echo ChainID: 456789 (dev mode)
echo.
start /B geth.exe --dev --http --http.addr 0.0.0.0 --http.port 8545 --http.api eth,web3,net,personal --http.corsdomain * --http.vhosts * --nodiscover --ipcdisable --dev.gaslimit 9999999999
echo Started!
echo MetaMask: http://localhost:8545 | ChainID: 456789
pause
