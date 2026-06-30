"""Auto-sync DB balance with on-chain WTC balance"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

w = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

old = '''    username = current_user.username
    eth_address, private_key = get_or_create_eth_account(username)
    if private_key is None:
        # External wallet - user manages their own key, fallback to off-chain
        pass
    user = wbankwallet.query.filter_by(username=username).first()
    balance = int(user.balance) if user else 0
    try:
        eth_balance = w3.eth.get_balance(eth_address)
        eth_balance_eth = w3.from_wei(eth_balance, 'ether')
    except:
        eth_balance_eth = 0
    return jsonify({'''

new = '''    username = current_user.username
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
    return jsonify({'''

if old in w:
    w = w.replace(old, new)
    print('[OK] Auto-sync added to web3_info')
else:
    print('[WARN] Pattern not found')
    idx = w.find('username = current_user.username')
    if idx >= 0:
        print(f'Found at {idx}:')
        print(w[idx:idx+400])

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')
print('\nRestart server')
