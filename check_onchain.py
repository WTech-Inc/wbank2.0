"""Check deployer on-chain activity and WTC balance"""
import sys, json
sys.stdout.reconfigure(encoding="utf-8")

from web3 import Web3
w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))
dep = Web3.to_checksum_address("0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7")
wtc = Web3.to_checksum_address("0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB")

block = w3.eth.block_number
print(f"Current block: {block}")

# Nonce (tx count)
nonce = w3.eth.get_transaction_count(dep)
print(f"Deployer nonce (sent tx count): {nonce}")

# ETH balance
eth_bal = w3.eth.get_balance(dep)
print(f"Deployer ETH: {w3.from_wei(eth_bal, 'ether')} ETH")

# WTC balance
min_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
c = w3.eth.contract(address=wtc, abi=min_abi)
bal = c.functions.balanceOf(dep).call()
print(f"Deployer WTC: {bal / 10**18} WTC")

# Check if contract has WTC balance (sent to contract address)
bal_con = c.functions.balanceOf(wtc).call()
print(f"Contract's own WTC balance (sent to itself): {bal_con / 10**18} WTC")
