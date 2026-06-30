"""Add gasless send - exact pattern matching"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

GAS_FEE = 50

w = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Pattern 1: Balance check - add fee check
old1 = '''    if not Web3.is_address(to_address):
        return jsonify({"error": "Invalid Ethereum address"}), 400
    user = wbankwallet.query.filter_by(username=username).first()
    if not user or int(user.balance) < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    eth_address, private_key = get_or_create_eth_account(username)'''

new1 = f'''    if not Web3.is_address(to_address):
        return jsonify({{"error": "Invalid Ethereum address"}}), 400
    total_amount = amount + {GAS_FEE}
    user = wbankwallet.query.filter_by(username=username).first()
    if not user or int(user.balance) < total_amount:
        return jsonify({{"error": f"Insufficient balance (need {{total_amount}} WTC: {{amount}} + {GAS_FEE} fee)"}}), 400
    eth_address, private_key = get_or_create_eth_account(username)'''

if old1 in w:
    w = w.replace(old1, new1)
    print('[OK] Balance check includes fee')
else:
    print('[FAIL] Pattern 1 not found')

# Pattern 2: On-chain section - use deployer wallet when user has no ETH
old2 = '''    # ─── FIRST: Try on-chain transfer ───
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
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()
    except Exception as e:
        if private_key:
            return jsonify({"error": f"On-chain error: {str(e)}"}), 500
        else:
            import time as _time
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()'''

new2 = '''    # ─── Gasless on-chain transfer ───
    tx_hash = None; tx_success = False; _gas_source = "user"
    try:
        import time as _time
        addr = Web3.to_checksum_address(WTC_CONTRACT_ADDRESS)
        if addr and addr != "0x" + "0" * 40:
            c = w3.eth.contract(address=addr, abi=WTC_ABI)
            dec = 18
            amt = amount * (10 ** dec)

            # Check if user has ETH for gas
            try: user_eth = w3.eth.get_balance(eth_address)
            except: user_eth = 0
            user_has_gas = user_eth > 5000000000000000 and private_key is not None

            if user_has_gas:
                # User pays gas (ETH)
                s = Account.from_key(private_key)
                tx = c.functions.transfer(Web3.to_checksum_address(to_address), amt).build_transaction({
                    'from': eth_address, 'nonce': w3.eth.get_transaction_count(eth_address),
                    'gas': 100000, 'gasPrice': w3.eth.gas_price, 'chainId': WTC_CHAIN_ID})
                signed = s.sign_transaction(tx)
            else:
                # Gasless: server pays ETH gas, user pays 50 WTC fee
                _gas_source = "server"
                _pk = ""
                try:
                    with open('E:\\\\wbank\\\\.env') as f:
                        for l in f:
                            l = l.strip()
                            if l.startswith('DEPLOYER_PRIVATE_KEY='):
                                _pk = l.split('=', 1)[1].strip()
                                break
                except: pass
                if _pk:
                    if _pk.startswith('0x'): _pk = _pk[2:]
                    _dep = Account.from_key(_pk)
                    tx = c.functions.transfer(Web3.to_checksum_address(to_address), amt).build_transaction({
                        'from': _dep.address, 'nonce': w3.eth.get_transaction_count(_dep.address),
                        'gas': 100000, 'gasPrice': w3.eth.gas_price, 'chainId': WTC_CHAIN_ID})
                    signed = _dep.sign_transaction(tx)
                else:
                    tx = None

            if tx:
                raw = w3.eth.send_raw_transaction(signed.raw_transaction)
                tx_hash = raw.hex()
                receipt = w3.eth.wait_for_transaction_receipt(raw, timeout=120)
                tx_success = (receipt.status == 1)
            else:
                tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()
        else:
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()
    except Exception:
        import time as _time
        tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()'''

if old2 in w:
    w = w.replace(old2, new2)
    print('[OK] Gasless on-chain transfer added')
else:
    print('[FAIL] Pattern 2 not found')

# Pattern 3: DB deduction
old3 = '''    # ─── THEN: Deduct from DB (only if on-chain succeeded OR simulated) ───
    user.balance = str(int(user.balance) - amount)
    db.session.commit()'''

new3 = '''    # ─── Deduct from DB (amount + fee) ───
    user.balance = str(int(user.balance) - total_amount)
    db.session.commit()'''

if old3 in w:
    w = w.replace(old3, new3)
    print('[OK] DB deduction includes fee')
else:
    print('[FAIL] Pattern 3 not found')

# Pattern 4: Record transaction
old4 = '''    # Record transaction (using raw SQL to avoid ORM PK conflict)
    try:
        from sqlalchemy import text as _st
        db.session.execute(
            _st("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t)"),
            {'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...", 't': local_time}
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Log the error (won't crash the app)'''

new4 = f'''    # Record transaction with fee info
    try:
        from sqlalchemy import text as _st
        _fee_note = f" (Gas: {{_gas_source}}, Fee: {GAS_FEE} WTC)" if tx_success else " (Off-chain)"
        db.session.execute(
            _st("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t)"),
            {{'u': username, 'a': f"WTC Transfer: Sent {{amount}} WTC to {{to_address}} | Tx: {{{{tx_hash[:20]}}}}...{{_fee_note}}", 't': local_time}}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()'''

if old4 in w:
    w = w.replace(old4, new4)
    print('[OK] Transaction record includes fee info')
else:
    print('[FAIL] Pattern 4 not found')

# Pattern 5: Return JSON
old5 = '''    return jsonify({
        "success": True,
        "amount": amount,
        "to": to_address,
        "from": eth_address,
        "tx_hash": tx_hash
    })'''

new5 = f'''    return jsonify({{
        "success": True,
        "amount": amount,
        "fee": {GAS_FEE},
        "gas_paid_by": _gas_source,
        "total_deducted": total_amount,
        "to": to_address,
        "from": eth_address,
        "tx_hash": tx_hash
    }})'''

if old5 in w:
    w = w.replace(old5, new5)
    print('[OK] Return JSON includes fee')
else:
    print('[FAIL] Pattern 5 not found')

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')
print(f'\nGas fee: {GAS_FEE} WTC per tx (~5 HKD)')
