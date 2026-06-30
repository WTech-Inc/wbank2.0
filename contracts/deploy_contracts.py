import os,sys,json,time
NETWORKS = {
    "bsc-testnet":{"chain_id":97,"rpc":"https://data-seed-prebsc-1-s1.binance.org:8545","explorer":"https://testnet.bscscan.com","currency":"tBNB","name":"BSC Testnet"},
    "sepolia":{"chain_id":11155111,"rpc":"https://ethereum-sepolia.publicnode.com","explorer":"https://sepolia.etherscan.io","currency":"ETH","name":"Sepolia"},
    "bsc-mainnet":{"chain_id":56,"rpc":"https://bsc-dataseed1.binance.org","explorer":"https://bscscan.com","currency":"BNB","name":"BSC Mainnet"}
}
net_name = sys.argv[1] if len(sys.argv)>1 else "eth-mainnet"
net = NETWORKS[net_name]
print(f"Deploying to {net['name']}...")
from web3 import Web3; from eth_account import Account
w3 = Web3(Web3.HTTPProvider(net["rpc"]))
if not w3.is_connected(): print("RPC failed"); sys.exit(1)
print(f"Connected (block {w3.eth.block_number})")
key = os.environ.get("DEPLOYER_PRIVATE_KEY","")
if key.startswith("0x"): key=key[2:]
if not key: print("Set DEPLOYER_PRIVATE_KEY"); sys.exit(1)
d = Account.from_key(key)
bal = w3.from_wei(w3.eth.get_balance(d.address),"ether")
print(f"Deployer: {d.address} ({bal} {net['currency']})")
# Compile
from solcx import compile_files, install_solc
install_solc("0.8.20",quiet=True)
cd = os.path.dirname(os.path.abspath(__file__))
compiled = compile_files([os.path.join(cd,"WTC.sol"),os.path.join(cd,"WTCBridge.sol")],
    solc_version="0.8.20",output_values=["abi","bin"],
    import_remappings=["@openzeppelin/contracts=../node_modules/@openzeppelin/contracts"])
wtc_a = next(v for k,v in compiled.items() if "WTC" in k and "Bridge" not in k)
br_a = next(v for k,v in compiled.items() if "Bridge" in k)
# Deploy WTC
print("\nDeploying WTC...")
WTC = w3.eth.contract(abi=wtc_a["abi"],bytecode=wtc_a["bin"])
tx = WTC.constructor().build_transaction({"from":d.address,"nonce":w3.eth.get_transaction_count(d.address),"gas":2000000,"gasPrice":w3.eth.gas_price,"chainId":net["chain_id"]})
s = d.sign_transaction(tx); h = w3.eth.send_raw_transaction(s.raw_transaction)
r = w3.eth.wait_for_transaction_receipt(h,120)
print(f"WTC: {r.contractAddress}")
# Deploy Bridge
print("\nDeploying Bridge...")
BR = w3.eth.contract(abi=br_a["abi"],bytecode=br_a["bin"])
tx2 = BR.constructor(r.contractAddress).build_transaction({"from":d.address,"nonce":w3.eth.get_transaction_count(d.address),"gas":2000000,"gasPrice":w3.eth.gas_price,"chainId":net["chain_id"]})
s2 = d.sign_transaction(tx2); h2 = w3.eth.send_raw_transaction(s2.raw_transaction)
r2 = w3.eth.wait_for_transaction_receipt(h2,120)
print(f"Bridge: {r2.contractAddress}")
# Configure
wtc = w3.eth.contract(address=r.contractAddress,abi=wtc_a["abi"])
if wtc.functions.bridgeAddress().call() != r2.contractAddress:
    tx3 = wtc.functions.setBridge(r2.contractAddress).build_transaction({"from":d.address,"nonce":w3.eth.get_transaction_count(d.address),"gas":50000,"gasPrice":w3.eth.gas_price,"chainId":net["chain_id"]})
    s3 = d.sign_transaction(tx3); w3.eth.send_raw_transaction(s3.raw_transaction); w3.eth.wait_for_transaction_receipt(w3.to_bytes(hexstr=w3.to_hex(w3.keccak(text=str(tx3)))),30)
    print("Bridge configured in WTC")
# Save
a = {"network":net_name,"chain_id":net["chain_id"],"wtc":{"address":r.contractAddress},"bridge":{"address":r2.contractAddress}}
p = os.path.join(cd,"deployments",f"{net_name}.json")
with open(p,"w") as f: json.dump(a,f,indent=2)
print(f"\nSaved to {p}")
print(f"\nDone! WTC: {r.contractAddress}\nBridge: {r2.contractAddress}\nExplorer: {net['explorer']}")
