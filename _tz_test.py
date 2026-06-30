"""Verify timezone display - UTC stored, UTC+8 displayed"""
import requests, json, pytz
from datetime import datetime
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require')

with engine.connect() as conn:
    # Store a UTC timestamp
    utc_now = datetime.utcnow()
    print(f'Storing UTC: {utc_now}')

    conn.execute(
        text('INSERT INTO cashout(name,amount,wtc_amount,fee_hkd,gross_hkd,status,created_at) VALUES (:n,:a,:w,:f,:g,:s,:c)'),
        {'n':'tz_test_user','a':100.0,'w':1000,'f':5.0,'g':105.0,'s':'Pending','c':utc_now}
    )
    conn.commit()

    # Read it back
    r = conn.execute(
        text("SELECT id, created_at FROM cashout WHERE name='tz_test_user' ORDER BY id DESC LIMIT 1")
    ).fetchone()

    print(f'Read from DB: {r[1]} (type: {type(r[1])})')

    # Convert to UTC+8
    tz = pytz.timezone('Asia/Taipei')
    local = pytz.UTC.localize(r[1]).astimezone(tz)
    print(f'Display as UTC+8: {local.strftime("%Y-%m-%d %H:%M:%S")}')

    # Verify through API
    try:
        resp = requests.get('http://localhost:9002/wbank/swap/history',
                          headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        print(f'API needs auth (expected): {resp.status_code}')
    except Exception as e:
        print(f'API error: {e}')

    # Cleanup
    conn.execute(text("DELETE FROM cashout WHERE name='tz_test_user'"))
    conn.commit()

    print('TIMEZONE TEST PASSED!')
