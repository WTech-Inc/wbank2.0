"""Add logout button + audit log for sends"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

# 1. Add logout button in top bar
old_top = '''    <div class="top-bar">
        <div class="title">WBank</div>
        <div class="user">{{ user.username }}<span> · 泓財銀行</span></div>
    </div>'''

new_top = '''    <div class="top-bar">
        <div class="title">WBank</div>
        <div class="user" style="display:flex;align-items:center;gap:12px;">
            <span>{{ user.username }}<span style="color:rgba(255,255,255,0.5);"> · 泓財銀行</span></span>
            <a href="/wbank/auth/v1/logout" style="font-size:12px;color:#ef4444;text-decoration:none;padding:4px 10px;border:1px solid rgba(239,68,68,0.3);border-radius:6px;">登出</a>
        </div>
    </div>'''

if old_top in tpl:
    tpl = tpl.replace(old_top, new_top)
    print('[OK] Logout button added to top bar')
else:
    print('[WARN] Top bar pattern not found')

# 2. Add audit log on send in wbank_web3.py if not already there
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Check if audit log exists for sends
if 'write_audit_log("WTC_SEND"' not in w3:
    # Add audit log before the return statement
    old_return = '''    return jsonify({{
        "success": True,
        "amount": amount,
        "fee": 50,
        "total_deducted": total_amount,
        "gas_paid_by": _gas_source,
        "to": to_address,
        "from": eth_address,
        "tx_hash": tx_hash
    }})'''

    new_return = '''    # Audit log
    try:
        write_audit_log("WTC_SEND", username, f"Sent {amount} WTC to {to_address} (Fee: 50, Gas: {_gas_source})", request)
    except:
        pass

    return jsonify({{
        "success": True,
        "amount": amount,
        "fee": 50,
        "total_deducted": total_amount,
        "gas_paid_by": _gas_source,
        "to": to_address,
        "from": eth_address,
        "tx_hash": tx_hash
    }})'''

    if old_return in w3:
        w3 = w3.replace(old_return, new_return)
        print('[OK] Audit log added to WTC send')
    else:
        print('[WARN] Return pattern not found')
else:
    print('[OK] Audit log already exists')

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

# 3. Also add logout route
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

logout_route = '''

@app.route("/wbank/auth/v1/logout")
def wbank_v1_logout():
    """Logout user."""
    from flask_login import logout_user
    logout_user()
    session.clear()
    return redirect("/wbank/auth/v1")
'''

if 'def wbank_v1_logout' not in m:
    # Insert before start_web
    idx = m.find('def start_web():')
    if idx > 0:
        m = m[:idx] + logout_route + m[idx:]
        open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)
        print('[OK] Logout route added')
else:
    print('[OK] Logout route already exists')

# Save wbankClient.html
open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8').write(tpl)

import py_compile
py_compile.compile('E:\\wbank\\main.py', doraise=True)
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')
print('Restart server')
