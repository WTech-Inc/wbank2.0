import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()
from solcx import compile_files, install_solc
install_solc("0.8.20")

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
print(f"Connected: {w3.is_connected()}, Block: {w3.eth.block_number}")

pk = ""
with open("E:\\wbank\\.env") as f:
    for line in f:
        line = line.strip()
        if line.startswith("DEPLOYER_PRIVATE_KEY="):
            pk = line.split("=", 1)[1].strip()
            break
if pk.startswith("0x"): pk = pk[2:]
dep = Account.from_key(pk)
print(f"Deployer: {dep.address}")

cd = "E:\\wbank\\contracts"
compiled = compile_files([os.path.join(cd, "WTC.sol")], solc_version="0.8.20", output_values=["abi", "bin"])
wtc_info = [v for k,v in compiled.items() if "WTC" in k and "Bridge" not in k][0]

nonce = w3.eth.get_transaction_count(dep.address)
WTC = w3.eth.contract(abi=wtc_info["abi"], bytecode=wtc_info["bin"])
tx = WTC.constructor().build_transaction({"from":dep.address,"nonce":nonce,"gas":2000000,"gasPrice":0,"chainId":456789})
signed = dep.sign_transaction(tx)
h = w3.eth.send_raw_transaction(signed.raw_transaction)
r = w3.eth.wait_for_transaction_receipt(h, timeout=120)
print(f"WTC deployed: {r.contractAddress} (gas used: {r.gasUsed}, gas price: 0)")

os.makedirs(os.path.join(cd, "deployments"), exist_ok=True)
with open(os.path.join(cd, "deployments", "private-chain.json"), "w") as f:
    json.dump({"chain_id":456789,"wtc":{"address":r.contractAddress}}, f, indent=2)
print("Done!")
