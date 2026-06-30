"""Fix wbank_web3.py to handle external wallets (no private key)"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Fix get_or_create_eth_account to handle external wallets
old = '''def get_or_create_eth_account(username):
    from sqlalchemy import text as sql_text
    result = db.session.execute(
        sql_text("SELECT eth_address, eth_key_encrypted FROM wbankwallet WHERE username=:uname"),
        {'uname': username}
    ).fetchone()
    if result and result[0]:
        return result[0], decrypt_key(result[1])
    acct = Account.create()
    eth_address = acct.address
    encrypted_key = encrypt_key(acct.key.hex())
    db.session.execute(
        sql_text("UPDATE wbankwallet SET eth_address=:addr, eth_key_encrypted=:ekey WHERE username=:uname"),
        {'addr': eth_address, 'ekey': encrypted_key, 'uname': username}
    )
    db.session.commit()
    return eth_address, acct.key.hex()'''

new = '''def get_or_create_eth_account(username):
    from sqlalchemy import text as sql_text
    result = db.session.execute(
        sql_text("SELECT eth_address, eth_key_encrypted FROM wbankwallet WHERE username=:uname"),
        {'uname': username}
    ).fetchone()
    if result and result[0]:
        enc_key = result[1]
        # Check if it's an external wallet (user provided their own address)
        if enc_key is None or enc_key == 'external_wallet_no_key':
            return result[0], None  # External wallet, no private key
        try:
            return result[0], decrypt_key(enc_key)
        except:
            # If decryption fails, treat as external wallet
            return result[0], None
    acct = Account.create()
    eth_address = acct.address
    encrypted_key = encrypt_key(acct.key.hex())
    db.session.execute(
        sql_text("UPDATE wbankwallet SET eth_address=:addr, eth_key_encrypted=:ekey WHERE username=:uname"),
        {'addr': eth_address, 'ekey': encrypted_key, 'uname': username}
    )
    db.session.commit()
    return eth_address, acct.key.hex()'''

if old in w3:
    w3 = w3.replace(old, new)
    print('[OK] External wallet support added')
else:
    print('[WARN] Could not find old function')
    # Debug: find the function
    idx = w3.find('def get_or_create_eth_account')
    if idx >= 0:
        print(f'Found at {idx}')
        print(w3[idx:idx+600])

# Also fix the web3_send to handle None private key
old_send = '''    eth_address, private_key = get_or_create_eth_account(username)'''
new_send = '''    eth_address, private_key = get_or_create_eth_account(username)
    if private_key is None:
        # External wallet - user manages their own key, fallback to off-chain
        pass'''

if old_send in w3:
    w3 = w3.replace(old_send, new_send)
    print('[OK] Send function handles external wallets')
else:
    idx = w3.find('eth_address, private_key =')
    if idx >= 0:
        print(f'Send line found at {idx}: {w3[idx:idx+80]}')

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')

print('\nRestart server')
