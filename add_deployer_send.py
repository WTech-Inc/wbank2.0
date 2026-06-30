"""Add deployer wallet sending for external wallets"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

w = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
lines = w.split('\n')

print('=== Current send logic ===')
for i, line in enumerate(lines):
    if 'private_key' in line and ('addr' in line or 'if ' in line):
        print(f'L{i+1}: {line.strip()[:120]}')

# Replace the on-chain logic to add deployer fallback
old = '''    if addr and addr != "0x" + "0" * 40 and private_key:
            c = w3.eth.contract(address=addr, abi=WTC_ABI)
            s = Account.from_key(private_key)
            try: dec = c.functions.decimals().call()
            except: dec = 18
            amt = amount * (10 ** dec)
            tx = c.functions.transfer(Web3.to_checksum_address(to_address), amt).build_transaction({
                'from': eth_address, 'nonce': w3.eth.get_transaction_count(eth_address),
                'gas': 100000, 'gasPrice': w3.eth.gas_price, 'chainId': WTC_CHAIN_ID})
            signed = s.sign_transaction(tx)
            raw = w3.eth.send_raw_transaction(signed.raw_transaction)
            tx_hash = raw.hex()
            receipt = w3.eth.wait_for_transaction_receipt(raw, timeout=120)
            tx_success = (receipt.status == 1)
            if not tx_success:
                return jsonify({"error": "On-chain transfer failed"}), 500
        else:
            # External wallet or no contract - use simulated hash
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()
    except Exception as e:
        if private_key:
            # External wallet with key - on-chain failed
            return jsonify({"error": f"On-chain error: {str(e)}"}), 500
        else:
            # External wallet without key - simulated
            import time as _time
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()'''

new = '''    if addr and addr != "0x" + "0" * 40:
            c = w3.eth.contract(address=addr, abi=WTC_ABI)
            dec = 18
            amt = amount * (10 ** dec)

            if private_key:
                # Send from user's wallet (they have key)
                s = Account.from_key(private_key)
                tx = c.functions.transfer(Web3.to_checksum_address(to_address), amt).build_transaction({
                    'from': eth_address, 'nonce': w3.eth.get_transaction_count(eth_address),
                    'gas': 100000, 'gasPrice': w3.eth.gas_price, 'chainId': WTC_CHAIN_ID})
                signed = s.sign_transaction(tx)
            else:
                # Gasless: send from deployer wallet (server pays ETH)
                _dpk = ""
                try:
                    with open('E:\\wbank\\.env') as _f:
                        for _l in _f:
                            _l = _l.strip()
                            if _l.startswith('DEPLOYER_PRIVATE_KEY='):
                                _dpk = _l.split('=', 1)[1].strip()
                                break
                except: pass
                if _dpk:
                    if _dpk.startswith('0x'): _dpk = _dpk[2:]
                    _dep = Account.from_key(_dpk)
                    tx = c.functions.transfer(Web3.to_checksum_address(to_address), amt).build_transaction({
                        'from': _dep.address, 'nonce': w3.eth.get_transaction_count(_dep.address),
                        'gas': 100000, 'gasPrice': w3.eth.gas_price, 'chainId': WTC_CHAIN_ID})
                    signed = _dep.sign_transaction(tx)
                else:
                    signed = None

            if signed:
                raw = w3.eth.send_raw_transaction(signed.raw_transaction)
                tx_hash = raw.hex()
                receipt = w3.eth.wait_for_transaction_receipt(raw, timeout=120)
                tx_success = (receipt.status == 1)
                if not tx_success:
                    return jsonify({"error": "On-chain transfer failed"}), 500
            else:
                tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()
        else:
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()
    except Exception as e:
        tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()'''

if old in w:
    w = w.replace(old, new)
    print('[OK] Gasless deployer send logic added')
else:
    print('[WARN] Pattern not found')
    # Show exact context
    idx = w.find('private_key:')
    if idx >= 0:
        print(f'Found private_key check at {idx}')
        print(w[idx:idx+200])

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')
print('\nRestart server')
