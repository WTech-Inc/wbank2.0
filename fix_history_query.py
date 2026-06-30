"""Fix history endpoint to use raw SQL (avoid ORM PK mismatch)"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Fix web3_history to use raw SQL
old_history = '''@web3_bp.route('/wbank/web3/history', methods=['GET'])
def web3_history():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    username = current_user.username
    records = wbankrecord.query.filter_by(username=username)\\
        .filter(wbankrecord.action.like("WTC%"))\\
        .order_by(wbankrecord.time.desc()).limit(20).all()
    return jsonify([{
        "action": r.action,
        "time": r.time.strftime("%Y/%m/%d %H:%M:%S") if r.time else ""
    } for r in records])'''

new_history = '''@web3_bp.route('/wbank/web3/history', methods=['GET'])
def web3_history():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    username = current_user.username
    try:
        # Use raw SQL to avoid ORM PK mismatch issues
        from sqlalchemy import text as _st
        records = db.session.execute(
            _st("SELECT action, time FROM wbankrecord WHERE username=:u AND action LIKE :p ORDER BY time DESC LIMIT 20"),
            {'u': username, 'p': 'WTC%'}
        ).fetchall()
        return jsonify([{
            "action": r[0],
            "time": r[1].strftime("%Y/%m/%d %H:%M:%S") if r[1] else ""
        } for r in records])
    except Exception:
        return jsonify([])'''

if old_history in w3:
    w3 = w3.replace(old_history, new_history)
    print('[OK] History endpoint fixed - uses raw SQL')
else:
    print('[WARN] Could not find old history')
    idx = w3.find('def web3_history')
    if idx >= 0:
        print(f'Found at {idx}')
        print(w3[idx:idx+300])

# Also remove the dummy _st("") call from send function
w3 = w3.replace('''        _st("")  # Dummy call to ensure import works
        db.session.execute(''', '''        db.session.execute(''')

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')

print('\nDone - restart server')
