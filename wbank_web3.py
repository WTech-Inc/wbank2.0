"""
WBank Web3 Module - ERC20 WTC Token
Real Ethereum account generation + transaction signing
"""
import os, json, hashlib, datetime, base64, pytz, pytz
from flask import Blueprint, request, jsonify, session
from web3 import Web3
from eth_account import Account
from cryptography.fernet import Fernet
from extensions import db
from models import *

Account.enable_unaudited_hdwallet_features()



# === WTC ERC20 Config (do_everything.py) ===
WTC_CONTRACT_ADDRESS = "0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB"
WTC_CHAIN_ID = 8453
WTC_RPC_URL = "https://mainnet.base.org"
WTC_ABI = [{"constant": False, "inputs": [{"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"}, {"constant": True, "inputs": [{"name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "type": "function"}, {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"}]

web3_bp = Blueprint('web3_bp', __name__)

# Network: BSC Testnet (changed from Sepolia)
SEPOLIA_RPC = "https://mainnet.base.org"
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))

ENCRYPTION_KEY = None

ENC_KEY_CACHE = None

def get_encryption_key():
    global ENC_KEY_CACHE
    if ENC_KEY_CACHE is None:
        raw = hashlib.sha256(b"WTech2225556").digest()
        ENC_KEY_CACHE = Fernet(base64.urlsafe_b64encode(raw))
    return ENC_KEY_CACHE

def encrypt_key(private_key_hex):
    k = get_encryption_key()
    return k.encrypt(private_key_hex.encode()).decode()

def decrypt_key(encrypted):
    k = get_encryption_key()
    return k.decrypt(encrypted.encode()).decode()

def get_or_create_eth_account(username):
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
    return eth_address, acct.key.hex()

@web3_bp.route('/wbank/web3/info', methods=['GET'])
def web3_info():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    username = current_user.username
    eth_address, private_key = get_or_create_eth_account(username)
    if private_key is None:
        pass
    user = wbankwallet.query.filter_by(username=username).first()
    balance = int(user.balance) if user else 0

    # Auto-sync: match DB balance to on-chain WTC
    try:
        bal_addr = Web3.to_checksum_address(WTC_CONTRACT_ADDRESS)
        if bal_addr and bal_addr != "0x" + "0" * 40:
            _bal_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')
            _bal_c = w3.eth.contract(address=bal_addr, abi=_bal_abi)
            onchain_bal = _bal_c.functions.balanceOf(eth_address).call()
            if user and int(user.balance) != int(onchain_bal / 10**18):
                user.balance = str(int(onchain_bal / 10**18))
                db.session.commit()
                balance = int(user.balance)
    except:
        pass

    try:
        eth_balance = w3.eth.get_balance(eth_address)
        eth_balance_eth = w3.from_wei(eth_balance, 'ether')
    except:
        eth_balance_eth = 0
    return jsonify({
        "address": eth_address,
        "balance": balance,
        "eth_balance": float(eth_balance_eth),
        "network": "Base Mainnet",
        "connected": w3.is_connected(),
        "token_name": "WCoins",
        "token_symbol": "WTC",
        "decimals": 18
    })

@web3_bp.route('/wbank/web3/send', methods=['POST'])
def web3_send():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    username = current_user.username
    to_address = request.json.get('to')
    amount = int(request.json.get('amount', 0))
    if not to_address or not amount:
        return jsonify({"error": "Missing parameters"}), 400
    if not Web3.is_address(to_address):
        return jsonify({"error": "Invalid Ethereum address"}), 400
    total_amount = amount + 50
    user = wbankwallet.query.filter_by(username=username).first()
    if not user or int(user.balance) < total_amount:
        return jsonify({"error": f"Insufficient balance (need {total_amount} WTC: {amount} + 50 fee)"}), 400
    eth_address, private_key = get_or_create_eth_account(username)
    _gas_source = "user" if private_key else "server"

    # ─── FIRST: Try on-chain transfer ───
    tx_hash = None; tx_success = False
    try:
        import time as _time
        addr = Web3.to_checksum_address(WTC_CONTRACT_ADDRESS)
        if addr and addr != "0x" + "0" * 40:
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
                    with open('E:\wbank\.env') as _f:
                        for _l in _f:
                            _l = _l.strip()
                            if _l.startswith('WCOINS_BANKER_PRIVATE_KEY=') or _l.startswith('DEPLOYER_PRIVATE_KEY='):
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
        tx_hash = "0x" + hashlib.sha256(f"{username}{to_address}{amount}{datetime.datetime.now()}{_time.time()}".encode()).hexdigest()

    # ─── Deduct from DB (amount + fee) ───
    user.balance = str(int(user.balance) - total_amount)
    db.session.commit()
    tz = pytz.timezone('Asia/Taipei')
    utc_time = datetime.datetime.now(pytz.timezone('UTC'))
    local_time = utc_time.astimezone(tz)
    # Record transaction with fee info
    try:
        from sqlalchemy import text as _st
        _fee_note = f" (Fee: 50 WTC)" if tx_success else " (Off-chain)"
        db.session.execute(
            _st("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t)"),
            {'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...{_fee_note}", 't': local_time}
        )
        db.session.commit()
    except Exception as _e:
        db.session.rollback()
        print(f"[WARN] Failed to save tx record: {_e}")
    return jsonify({
        "success": True,
        "amount": amount,
        "fee": 50,
        "total_deducted": total_amount,
        "gas_paid_by": _gas_source,
        "to": to_address,
        "from": eth_address,
        "tx_hash": tx_hash
    })

@web3_bp.route('/wbank/web3/history', methods=['GET'])
def web3_history():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    username = current_user.username
    try:
        # Use raw SQL to avoid ORM PK mismatch issues
        from sqlalchemy import text as _st
        records = db.session.execute(
            _st("SELECT action, time FROM wbankrecord WHERE username=:u AND (action LIKE :p OR action LIKE 'SWAP%') ORDER BY time DESC LIMIT 20"),
            {'u': username, 'p': 'WTC%'}
        ).fetchall()
        return jsonify([{
            "action": r[0],
            "time": r[1].strftime("%Y/%m/%d %H:%M:%S") if r[1] else ""
        } for r in records])
    except Exception:
        return jsonify([])


# CSRF exemption
web3_info._csrf_exempt = True
web3_send._csrf_exempt = True
web3_history._csrf_exempt = True
