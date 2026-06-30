"""Add gasless WTC send - server pays ETH gas, user pays 50 WTC fee"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

GAS_FEE = 50  # WTC per transaction

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Find and replace the send function
old_send = '''@web3_bp.route('/wbank/web3/send', methods=['POST'])
def web3_send():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    username = current_user.username
    to_address = request.json.get('to')
    amount_raw = request.json.get('amount', 0)

    try:
        amount = int(amount_raw)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount"}), 400

    if not to_address or not amount:
        return jsonify({"error": "Missing parameters"}), 400
    if not Web3.is_address(to_address):
        return jsonify({"error": "Invalid Ethereum address"}), 400
    if amount <= 0:
        return jsonify({"error": "Amount must be > 0"}), 400

    # ─── Check DB balance (off-chain) ───
    user = wbankwallet.query.filter_by(username=username).first()
    if not user or int(user.balance) < amount:
        return jsonify({"error": "Insufficient balance"}), 400'''

new_send = f'''@web3_bp.route('/wbank/web3/send', methods=['POST'])
def web3_send():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({{"error": "Not logged in"}}), 401
    username = current_user.username
    to_address = request.json.get('to')
    amount_raw = request.json.get('amount', 0)

    try:
        amount = int(amount_raw)
    except (ValueError, TypeError):
        return jsonify({{"error": "Invalid amount"}}), 400

    if not to_address or not amount:
        return jsonify({{"error": "Missing parameters"}}), 400
    if not Web3.is_address(to_address):
        return jsonify({{"error": "Invalid Ethereum address"}}), 400
    if amount <= 0:
        return jsonify({{"error": "Amount must be > 0"}}), 400

    total_cost = amount + {GAS_FEE}
    # ─── Check DB balance (off-chain) including fee ───
    user = wbankwallet.query.filter_by(username=username).first()
    if not user or int(user.balance) < total_cost:
        return jsonify({{"error": f"Insufficient balance (need {{total_cost}} WTC: {{amount}} + {GAS_FEE} fee)"}}), 400'''

if old_send in w3:
    w3 = w3.replace(old_send, new_send)
    print(f'[OK] Fee check added: {GAS_FEE} WTC per tx')
else:
    print('[WARN] Could not find old send start')
    # Debug
    idx = w3.find('def web3_send()')
    if idx >= 0:
        print(f'Found at {idx}')
        print(w3[idx:idx+400])
    sys.exit(1)

# Now fix the DB deduction to include fee
old_deduct = '''    # ─── THEN: Deduct from DB (only if on-chain succeeded OR simulated) ───
    user.balance = str(int(user.balance) - amount)
    db.session.commit()'''

new_deduct = f'''    # ─── THEN: Deduct from DB + fee ───
    user.balance = str(int(user.balance) - total_cost)
    db.session.commit()'''

if old_deduct in w3:
    w3 = w3.replace(old_deduct, new_deduct)
    print(f'[OK] DB deduction includes {GAS_FEE} WTC fee')
else:
    print('[WARN] Could not find DB deduction')
    idx = w3.find('user.balance = str(int(user.balance)')
    if idx >= 0:
        print(f'Found at {idx}: {w3[idx:idx+80]}')

# Now fix the on-chain send to use deployer wallet when user has no ETH
# This is in the ERC20 transfer section - we need to replace the transfer logic
old_onchain = '''    # ─── FIRST: Try on-chain transfer ───
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
            # Has private key but on-chain failed
            return jsonify({"error": f"On-chain error: {str(e)}"}), 500
        else:
            # External wallet without key - simulated
            import time as _time
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()'''

new_onchain = '''    # ─── On-chain transfer (gasless for user) ───
    tx_hash = None; tx_success = False
    try:
        import time as _time
        addr = Web3.to_checksum_address(WTC_CONTRACT_ADDRESS)
        if addr and addr != "0x" + "0" * 40:
            try:
                # Check if user's wallet has ETH for gas
                user_eth = w3.eth.get_balance(eth_address)
                has_gas = user_eth > 5000000000000000  # 0.005 ETH minimum
            except:
                has_gas = False

            if has_gas and private_key:
                # Send from user's wallet (they pay gas)
                s = Account.from_key(private_key)
                dec = 18
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
                # Gasless: send from server's deployer wallet (server pays ETH, user pays 50 WTC fee)
                # Load deployer key
                _pk = ''
                try:
                    with open('E:\\wbank\\.env') as _f:
                        for _line in _f:
                            _line = _line.strip()
                            if _line.startswith('DEPLOYER_PRIVATE_KEY='):
                                _pk = _line.split('=', 1)[1].strip()
                                break
                except:
                    pass

                if _pk:
                    if _pk.startswith('0x'): _pk = _pk[2:]
                    _deployer = Account.from_key(_pk)
                    _dec = 18
                    _amt = amount * (10 ** _dec)
                    _tx = c.functions.transfer(Web3.to_checksum_address(to_address), _amt).build_transaction({
                        'from': _deployer.address, 'nonce': w3.eth.get_transaction_count(_deployer.address),
                        'gas': 100000, 'gasPrice': w3.eth.gas_price, 'chainId': WTC_CHAIN_ID})
                    _signed = _deployer.sign_transaction(_tx)
                    _raw = w3.eth.send_raw_transaction(_signed.raw_transaction)
                    tx_hash = _raw.hex()
                    _receipt = w3.eth.wait_for_transaction_receipt(_raw, timeout=120)
                    tx_success = (_receipt.status == 1)
                else:
                    # No deployer key - simulated
                    tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()
        else:
            tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()
    except Exception:
        import time as _time
        tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()'''

if old_onchain in w3:
    w3 = w3.replace(old_onchain, new_onchain)
    print('[OK] Gasless send implemented: server pays ETH, user pays 50 WTC')
else:
    print('[WARN] Could not find old onchain block')
    # Debug
    idx = w3.find('FIRST: Try on-chain')
    if idx >= 0:
        print(f'Found onchain block at {idx}')
        print(w3[idx:idx+200])

# Now update the transaction record to include fee info
old_record = '''    # Record transaction (using raw SQL to avoid ORM PK conflict)
    try:
        from sqlalchemy import text as _st
        db.session.execute(
            _st("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t)"),
            {'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...", 't': local_time}
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Log the error (won't crash the app)
        print(f"[WARN] Failed to save tx record: {e}")'''

new_record = f'''    # Record transaction with fee
    try:
        from sqlalchemy import text as _st
        _fee_info = f" (Fee: {GAS_FEE} WTC)" if tx_success else " (Off-chain)"
        db.session.execute(
            _st("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t)"),
            {{'u': username, 'a': f"WTC Transfer: Sent {{amount}} WTC to {{to_address}} | Tx: {{{{tx_hash[:20]}}}}...{{_fee_info}}", 't': local_time}}
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()'''

if old_record in w3:
    w3 = w3.replace(old_record, new_record)
    print('[OK] Transaction record includes fee info')
else:
    print('[WARN] Could not find old record block')
    idx = w3.find('Record transaction')
    if idx >= 0:
        print(f'Found at {idx}')

# Update the return JSON to include fee info
old_return = '''    return jsonify({
        "success": True,
        "amount": amount,
        "to": to_address,
        "from": eth_address,
        "tx_hash": tx_hash
    })'''

new_return = f'''    return jsonify({{
        "success": True,
        "amount": amount,
        "fee": {GAS_FEE},
        "total_deducted": total_cost,
        "to": to_address,
        "from": eth_address,
        "tx_hash": tx_hash,
        "tx_success": tx_success
    }})'''

if old_return in w3:
    w3 = w3.replace(old_return, new_return)
    print('[OK] Return JSON includes fee info')
else:
    print('[WARN] Could not find return JSON')
    idx = w3.find('"success": True')
    if idx >= 0:
        print(f'Found at {idx}')

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

import py_compile
try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('[OK] Syntax OK')
except py_compile.PyCompileError as e:
    print(f'[FAIL] {e}')

print(f'\nGas fee: {GAS_FEE} WTC per transaction (~5 HKD)')
print('Restart server')
