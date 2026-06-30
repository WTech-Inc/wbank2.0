"""Clean up gasless send bugs"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

w = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Fix 1: Add _gas_source definition after private_key check
old = '''    eth_address, private_key = get_or_create_eth_account(username)

    # ─── FIRST: Try on-chain transfer ───'''
new = '''    eth_address, private_key = get_or_create_eth_account(username)
    _gas_source = "user" if private_key else "server"

    # ─── FIRST: Try on-chain transfer ───'''
w = w.replace(old, new)

# Fix 2: Fix TX record f-string (double braces)
old2 = '''{'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {{tx_hash[:20]}}...{_fee_note}", 't': local_time}'''
new2 = '''{'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...{_fee_note}", 't': local_time}'''
w = w.replace(old2, new2)

# Fix 3: Fix except clause
old3 = '''    except Exception:
        db.session.rollback()
        print(f"[WARN] Failed to save tx record: {e}")'''
new3 = '''    except Exception as _e:
        db.session.rollback()
        print(f"[WARN] Failed to save tx record: {_e}")'''
w = w.replace(old3, new3)

# Fix 4: Clean up return JSON - remove duplicates
old4 = '''    return jsonify({
        "success": True,
        "fee": 50,
        "total_deducted": total_amount,
        "amount": amount,
        "fee": 50,
        "gas_paid_by": _gas_source,
        "total_deducted": total_amount,
        "to": to_address,
        "from": eth_address,
        "tx_hash": tx_hash
    })'''
new4 = '''    return jsonify({
        "success": True,
        "amount": amount,
        "fee": 50,
        "total_deducted": total_amount,
        "gas_paid_by": _gas_source,
        "to": to_address,
        "from": eth_address,
        "tx_hash": tx_hash
    })'''
w = w.replace(old4, new4)

# Fix 5: Remove duplicate fee_note for non-tx_success
old5 = '_fee_note = f" (Gas: {_gas_source}, Fee: 50 WTC)" if tx_success else " (Off-chain)"'
new5 = '_fee_note = f" (Fee: 50 WTC)" if tx_success else " (Off-chain)"'
w = w.replace(old5, new5)

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] All bugs fixed + syntax OK')

# Show final send function
lines = w.split('\n')
for i in range(104, 185):
    if i < len(lines):
        print(f'L{i+1}: {lines[i]}')
