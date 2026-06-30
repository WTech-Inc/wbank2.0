"""Fix insert to use raw SQL (avoid ORM primary key issue)"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Find and fix the INSERT section
old_section = '''    # Record transaction
    try:
        from sqlalchemy import text as _sql_text
        db.session.add(wbankrecord(
            username=username,
            action=f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...",
            time=local_time
        ))
        db.session.commit()
    except Exception:
        try:
            db.session.rollback()
            # Fallback: use raw SQL
            from sqlalchemy import text as _sql_text2
            db.session.execute(
                _sql_text2("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t)"),
                {'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...", 't': local_time}
            )
            db.session.commit()
        except:
            db.session.rollback()'''

new_section = '''    # Record transaction (using raw SQL to avoid ORM PK conflict)
    try:
        from sqlalchemy import text as _st
        _st("")  # Dummy call to ensure import works
        db.session.execute(
            _st("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t)"),
            {'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...", 't': local_time}
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Log the error (won't crash the app)
        print(f"[WARN] Failed to save tx record: {e}")'''

if old_section in w3:
    w3 = w3.replace(old_section, new_section)
    print('[OK] Fixed INSERT to use raw SQL')
else:
    print('[WARN] Could not find old section')
    # Debug
    idx = w3.find('Record transaction')
    if idx >= 0:
        print(f'Found at {idx}:')
        print(w3[idx:idx+400])

open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)

import py_compile
py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
print('[OK] Syntax OK')

# Also update models.py to fix primary key
print('\nChecking models.py...')
mod = open('E:\\wbank\\models.py', 'r', encoding='utf-8').read()
if 'class wbankrecord' in mod:
    # Find the model and check its pk
    lines = mod.split('\n')
    for i, line in enumerate(lines):
        if 'class wbankrecord' in line:
            for j in range(i, min(i+10, len(lines))):
                print(f'  L{j+1}: {lines[j]}')
            break
else:
    print('  wbankrecord model not in models.py (might be in main.py)')

print('\nDone - restart server')
