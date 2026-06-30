import sys
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ethereum-rpc.publicnode.com'))
addr = Web3.to_checksum_address('0xdffA9CFE9FFA749Fd93883c587193381263AA59c')
eth = w3.eth.get_balance(addr)
print(f'Mainnet ETH: {w3.from_wei(eth, "ether")}')

# Also check Sepolia
w3s = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))
eth_s = w3s.eth.get_balance(addr)
print(f'Sepolia ETH: {w3s.from_wei(eth_s, "ether")}')
