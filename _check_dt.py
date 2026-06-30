"""Check SQLAlchemy datetime type and pytz conversion"""
import sys
sys.path.insert(0, 'E:\\wbank')
sys.modules.pop('wcoins_blockchain', None)

# Don't import main.py - just use psycopg2 directly
import psycopg2, pytz, datetime

conn = psycopg2.connect(
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech',
    dbname='neondb', user='neondb_owner',
    password='npg_KP2Zat1YscBz', sslmode='require'
)
cur = conn.cursor()
cur.execute('SELECT block_index, created_at FROM wcoins_block ORDER BY block_index DESC LIMIT 1')
r = cur.fetchone()
raw_dt = r[1]
print(f'Raw type: {type(raw_dt).__name__}')
print(f'Raw value: {raw_dt}')
print(f'tzinfo: {raw_dt.tzinfo}')
print(f'Has tz: {raw_dt.tzinfo is not None}')

# Method 1: pytz.UTC.localize
result1 = pytz.UTC.localize(raw_dt).astimezone(pytz.timezone('Asia/Taipei'))
print(f'Method 1 (localize): {result1.strftime("%Y-%m-%d %H:%M:%S")}')

# Method 2: replace + astimezone
result2 = raw_dt.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Taipei'))
print(f'Method 2 (replace): {result2.strftime("%Y-%m-%d %H:%M:%S")}')

# Method 3: timedelta
result3 = (raw_dt + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
print(f'Method 3 (timedelta): {result3}')

cur.close()
conn.close()
