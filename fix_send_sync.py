"""Fix send function: on-chain first, then DB (keep them in sync)"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Find the current send function's DB deduction and replace it
old_send_logic = '''    user = wbankwallet.query.filter_by(username=username).first()
    if not user or int(user.balance) < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    eth_address, private_key = get_or_create_eth_account(username)
    if private_key is None:
        # External wallet - user manages their own key, fallback to off-chain
        pass
    user.balance = str(int(user.balance) - amount)
    db.session.commit()
    # ─── ERC20 WTC Transfer ───
    tx_hash = None; tx_success = False
    try:
        import time as _time
        addr = Web3.to_checksum_address(WTC_CONTRACT_ADDRESS)
        if addr and addr != "0x" + "0" * 40:
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
        else:
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()
    except Exception:
        import time as _time
        tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()'''

new_send_logic = '''    user = wbankwallet.query.filter_by(username=username).first()
    if not user or int(user.balance) < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    eth_address, private_key = get_or_create_eth_account(username)

    # ─── FIRST: Try on-chain transfer ───
    tx_hash = None; tx_success = False
    try:
        import time as _time
        addr = Web3.to_checksum_address(WTC_CONTRACT_ADDRESS)
        if addr and addr != "0x" + "0" * 40 and private_key:
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
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()

    # ─── THEN: Deduct from DB (only if on-chain succeeded OR simulated) ───
    user.balance = str(int(user.balance) - amount)
    db.session.commit()'''

if old_send_logic in w3:
    w3 = w3.replace(old_send_logic, new_send_logic)
    print('[OK] Send logic updated: on-chain first, then DB')
else:
    print('[WARN] Could not find old send logic')
    # Debug: find the relevant section
    idx = w3.find('Insufficient balance')
    if idx >= 0:
        print(f'Found at {idx}:')
        print(w3[idx:idx+100])
    idx = w3.find('tx_success = (receipt.status == 1)')
    if idx >= 0:
        print(f'\ntx_success found at {idx}')

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')
print('\nRestart server')
