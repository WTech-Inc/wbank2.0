@echo off
cd /d E:\wbank\private-chain
echo ===================================
echo   部署 WTC Token
echo ===================================
echo.
echo 請確保節點已在運行 (第1步已做)
echo.
python deploy_wtc.py
echo.
pause
