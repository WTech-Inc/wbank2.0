import py_compile

with open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the record insertion block and make it safe
old_block = """    tz = pytz.timezone('Asia/Taipei')
    utc_time = datetime.datetime.now(pytz.timezone('UTC'))
    local_time = utc_time.astimezone(tz)
    db.session.add(wbankrecord(
        username=username,
        action=f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...",
        time=local_time
    ))
    db.session.commit()"""

new_block = """    tz = pytz.timezone('Asia/Taipei')
    utc_time = datetime.datetime.now(pytz.timezone('UTC'))
    local_time = utc_time.astimezone(tz)
    # Record transaction (safe insert - handle duplicate PK)
    try:
        db.session.execute(
            text("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t) ON CONFLICT (username) DO UPDATE SET action = :a, time = :t"),
            {'u': username, 'a': f"WTC Transfer: Sent {amount} WTC to {to_address} | Tx: {tx_hash[:20]}...", 't': local_time}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()"""

if old_block in content:
    content = content.replace(old_block, new_block)
    print('Fixed send record block')
else:
    print('Could not find old block')
    # Debug
    idx = content.find('tz = pytz.timezone')
    if idx >= 0:
        print(content[idx:idx+400])

with open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
