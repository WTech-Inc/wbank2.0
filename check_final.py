import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))
user = '0x53A081aeedD98D82ef29ed93818a501E2CeD2209'
eth_bal = w3.eth.get_balance(user)
print(f'User ETH: {w3.from_wei(eth_bal, "ether")}')

# Check WTC balance
wtc_addr = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
c = w3.eth.contract(address=Web3.to_checksum_address(wtc_addr), abi=abi)
try:
    wtc_bal = c.functions.balanceOf(Web3.to_checksum_address(user)).call()
    print(f'User WTC: {wtc_bal / 10**18:,.0f}')
except Exception as e:
    print(f'WTC: {e}')
