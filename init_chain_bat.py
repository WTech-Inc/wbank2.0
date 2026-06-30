"""Write and run batch file to init chain"""
import sys, subprocess, os
sys.stdout.reconfigure(encoding='utf-8')

# Write batch file
bat = '''@echo off
cd /d E:\\wbank\\private-chain
echo Init chain...
E:\\wbank\\private-chain\\geth.exe --datadir E:\\wbank\\private-chain\\data init E:\\wbank\\private-chain\\genesis.json
echo EXIT CODE: %ERRORLEVEL%
if exist E:\\wbank\\private-chain\\data\\geth\\chaindata (
  echo SUCCESS: Chain initialized
) else (
  echo FAIL: Chain not initialized
)
pause
'''

with open('E:\\wbank\\private-chain\\init.bat', 'w') as f:
    f.write(bat)

print('Running init.bat...')
result = subprocess.run('E:\\wbank\\private-chain\\init.bat', capture_output=True, text=True, timeout=120, shell=True)
print(result.stdout[-500:])
if result.stderr:
    print('ERR:', result.stderr[-500:])
